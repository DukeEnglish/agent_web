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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    '''ChatGPT Prompt'''
    print(request.json)
    user_input = request.json.get('message', [])
    llm_service_name = request.json.get(
        'llmservice', DEFAULT_LLM_SERVICE_NAME)
    api_key = request.json.get('apikey', DEFAULT_API_KEY)

    headers = {'Authorization': f'Bearer {api_key}'}
    llm_client = ServiceFactory().get_service(llm_service_name)
    print("input is ", user_input, request.method)


    if request.method == 'POST':
        
        response = llm_client.llm_stream(user_input=user_input)

        messages = []
        for line in response:
            messages.append({"userMessage": user_input, "botMessage": line})

        return json.dumps(messages)

    def generate():
        response = llm_client.llm_stream(user_input=user_input)

        for line in response:
            time.sleep(0.5)
            print(
                f'{json.dumps({"userMessage": user_input, "botMessage": line})}\n\n')
            yield f'{json.dumps({"userMessage": user_input, "botMessage": line})}\n\n'

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)
