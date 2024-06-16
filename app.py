# app.py
from flask import Flask, render_template, request, Response
from llm_service import ServiceFactory
from flask_cors import CORS
import json
import time

app = Flask(__name__)
CORS(app)  # 允许所有域名访问

# 默认设置
DEFAULT_LLM_SERVICE_NAME = 'glm'
DEFAULT_API_KEY = 'default-api-key'
DEFAULT_SEC_KEY = 'default-sec-key'
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
    HISTORY[user_id][:-1] += dialogue


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    '''ChatGPT Prompt'''
    print(request.json)
    user_input = request.json.get('message', [])
    llm_service_name = request.json.get(
        'llmservice', DEFAULT_LLM_SERVICE_NAME)
    api_key = request.json.get('apikey', DEFAULT_API_KEY)
    sec_key = request.json.get('seckey', DEFAULT_SEC_KEY)
    user_id = request.json.get('userId', DEFAULT_SEC_KEY)

    # headers = {'Authorization': f'Bearer {api_key}'}
    llm_client = ServiceFactory().get_service(llm_service_name, api_key, sec_key)
    messages_list = get_dialogue(user_id=user_id, user_input=user_input)
    print("111", messages_list)

    if request.method == 'POST':

        response = llm_client.chat_stream(messages_list)

        messages = []
        history = []
        for line in response:
            messages.append({"userMessage": user_input, "botMessage": line})
            history.append(line)
        update_history(user_id, ''.join(history))
        return json.dumps(messages)

    def generate():
        response = llm_client.chat_stream(messages_list)
        messages = []

        for line in response:
            time.sleep(0.5)
            print(
                f'{json.dumps({"userMessage": user_input, "botMessage": line})}\n\n')
            bot_message = f'{json.dumps({"userMessage": user_input, "botMessage": line})}\n\n'
            messages.append(bot_message)
            yield bot_message
        # update_history(user_id, messages)
    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)
