# app.py
import sys
sys.path.append("../")
import time
import json
from code_ana.ana_code import process
from flask_cors import CORS
from llm_service import ServiceFactory
from flask import Flask, render_template, request, Response, stream_with_context, jsonify


app = Flask(__name__)
CORS(app)  # 允许所有域名访问

# 默认设置
DEFAULT_LLM_SERVICE_NAME = 'glm'
DEFAULT_API_KEY = 'default-api-key'
DEFAULT_SEC_KEY = 'default-sec-key'
DEFAULT_GITHUB_URL = 'git@github.com:DukeEnglish/miniagent.git'
HISTORY = {}


@app.route('/')
def index():
    return render_template('index.html')


def get_dialogue(user_id, user_input):
    """存储历史对话, 当前仅支持内存存储，所以仅以userid区分

    """
    current_dialogue = [{
                        "role": "user",
                        "content": f"{user_input}"
                        }]
    if user_id not in HISTORY:
        HISTORY[user_id] = []
    HISTORY[user_id] += current_dialogue
    return HISTORY[user_id]


def update_history(user_id, bot_response):
    """
    历史对话构造，首轮背景保留，最近3轮保留

    Args:
        user_id (_type_): _description_
    """

    current_user_input = HISTORY[user_id][-1]
    # reconstruct history 因为太长了
    len_history = len(HISTORY[user_id]) 
    if len_history > 10:
        background = HISTORY[user_id][:2]  # 保留用户第一个问题和机器的答案
        last_three = []
        last_three = HISTORY[user_id][-7:-1]  # 保留用户最近三轮
        current_user_input = HISTORY[user_id][-1],
        HISTORY[user_id] = background + last_three
    # add new
    dialogue = [
        current_user_input,
        {
            "role": "assistant",
            "content": f"{bot_response}"
        }
    ]
    HISTORY[user_id] = HISTORY[user_id][:-1] + dialogue
    print("his up", HISTORY)


llm_client = None
messages_list = None
user_id = None


@app.route('/chat', methods=['POST', 'GET'])
def chat_code():
    print(request)
    if request.method == 'POST':
        '''ChatGPT Prompt'''
        print(request.json)
        global llm_client
        global messages_list
        global user_id
        user_input = request.json.get('message', [])
        llm_service_name = request.json.get(
            'llmservice', DEFAULT_LLM_SERVICE_NAME)
        api_key = request.json.get('apikey', DEFAULT_API_KEY)
        sec_key = request.json.get('seckey', DEFAULT_SEC_KEY)
        user_id = request.json.get('userId', DEFAULT_SEC_KEY)
        user_id = request.json.get('userId', DEFAULT_SEC_KEY)
        github = request.json.get('github', DEFAULT_GITHUB_URL)
        llm_client = ServiceFactory().get_service(llm_service_name, api_key, sec_key)
        messages_list = get_dialogue(user_id=user_id, user_input=user_input)
        messages_list = process(messages_list, github)
        print(messages_list)
    if request.method == 'GET':

        def generate():
            # if messages_list:
            response = llm_client.chat_stream(messages_list)
            messages = []

            for line, is_complete in response:
                time.sleep(0.5)
                print(
                    f'{json.dumps({"botMessage": line})}\n\n')
                if not line:
                    update_history(user_id, messages)
                    bot_message = json.dumps({"botMessage": "", 'isComplete': is_complete})
                else:
                    bot_message = json.dumps({"botMessage": line, 'isComplete': is_complete})
                    messages.append(line)
                yield f'data: {bot_message}\n\n'
        return Response(stream_with_context(generate()), mimetype='text/event-stream')

    else:
        return jsonify({'status': 'Message sent successfully'})


if __name__ == '__main__':
    app.run(debug=True)
