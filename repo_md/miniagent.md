## `app.py`
```text
# app.py
from flask import Flask, render_template, request, Response
from llm_service.glm import glm_client
from flask_cors import CORS
import json
import time

app = Flask(__name__)
CORS(app)  # 允许所有域名访问

# 默认设置
DEFAULT_LLM_SERVICE_URL = 'https://default-llm-service.com/api'
DEFAULT_API_KEY = 'default-api-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    '''ChatGPT Prompt'''
    if request.method == 'POST':
        user_input = request.json.get('message', [])
        llm_service_url = request.json.get('llmservice', DEFAULT_LLM_SERVICE_URL)
        api_key = request.json.get('apikey', DEFAULT_API_KEY)

        headers = {'Authorization': f'Bearer {api_key}'}
        response = glm_client.llm_stream(user_input=user_input)

        messages = []
        for line in response:
            messages.append({"userMessage": user_input, "botMessage": line})

        return json.dumps(messages)

    def generate():
        user_input = request.args.get('message', [])
        llm_service_url = request.args.get('llmservice', DEFAULT_LLM_SERVICE_URL)
        api_key = request.args.get('apikey', DEFAULT_API_KEY)

        headers = {'Authorization': f'Bearer {api_key}'}
        response = glm_client.llm_stream(user_input=user_input)

        for line in response:
            time.sleep(0.5)
            print(f'data: {json.dumps({"userMessage": user_input, "botMessage": line})}\n\n')
            yield f'data: {json.dumps({"userMessage": user_input, "botMessage": line})}\n\n'

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
```

## `main.js`
```js
// static/js/main.js
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
}

// 新写的函数，用于根据发送者自动调整消息位置
function adjustMessagePosition(messageDiv, isBot) {
    if (isBot) {
        messageDiv.style.float = 'left';
    } else {
        messageDiv.style.float = 'right';
    }
}

/* 新写的函数，用于添加消息到聊天历史 */
function addMessageToChatHistory(message, isBot) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-bubble');
    if (isBot) {
        messageDiv.classList.add('bot-bubble');
    } else {
        messageDiv.classList.add('user-bubble');
    }
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    // 滚动到底部
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const githubUrl = document.getElementById('github-url').value || null;
    const llmservice = document.getElementById('llmservice-select').value || 'https://default-llm-service.com/api';
    const apikey = document.getElementById('apikey').value || null;

    if (!userInput) {
        alert('Please enter a message.');
        return;
    }

    const chatBox = document.getElementById('chat-box');
    const userMessage = document.createElement('div');
    userMessage.classList.add('chat-bubble', 'user-bubble');
    userMessage.textContent = userInput;
    adjustMessagePosition(userMessage, false); // 用户消息
    // chatBox.insertBefore(userMessage, chatBox.firstChild);
    chatBox.appendChild(userMessage); // 将新消息追加到聊天框的末尾
    chatBox.scrollTop = chatBox.scrollHeight; // 滚动到底部

    const payload = {
        message: userInput,
        llmservice: llmservice,
        apikey: apikey,
        github: githubUrl
    };

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        response.json().then(data => {
            console.log("test", typeof(data), data)
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('bot-message');
            data.forEach(item => {
                messageDiv.textContent += item.botMessage;
                const chatBox = document.getElementById('chat-box');
                
                chatBox.appendChild(messageDiv);
                // 根据isBot的值调整消息位置
                adjustMessagePosition(messageDiv, item.isBot);
                // 滚动到底部
                chatBox.scrollTop = chatBox.scrollHeight;
            });
            
        });
    })

    .catch(error => console.error('Error:', error));

    document.getElementById('user-input').value = '';
}

// 新写的函数，用于初始化和监听 SSE（Server-Sent Events）
function initEventSource() {
    const eventSource = new EventSource('/chat');

    eventSource.onmessage = function(event) {
        // 解析 JSON 数据
        const messageObj = JSON.parse(event.data);
        addMessageToChatHistory(messageObj.text, messageObj.isBot); 
    };

    eventSource.onerror = function(event) {
        console.error('EventSource failed:', event);
        eventSource.close();
    };
}

function clearChatHistory() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
}
```

## `index.html`
```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Interface</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>

<body>
    <div class="container">
        <div class="chat-container">
            <div class="chat-area">
                <div class="chat-history" id="chat-box">
                    <div class="chat-pair">
                        <!-- <div class="chat-bubble bot-bubble">你好，我是A。</div> -->
                        <!-- <div class="chat-bubble user-bubble">你好，机器人。</div> -->
                    </div>
                </div>
                <div class="chat-input-area">
                    <input id="user-input" type="text" placeholder="Type your message here..."
                        onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
            <div class="sidebar">
                <!-- <div class="settings-container"> -->
                    <div class="options-sidebar">
                        <h2>Settings</h2>
                        <label for="github-url">GitHub URL (optional):</label>
                        <input id="github-url" type="text" placeholder="GitHub URL">
                        <label for="llmservice-select">LLM Service:</label>
                        <select id="llmservice-select">
                            <option value="">Select LLM Service</option>
                            <option value="https://baidu-llm-service.com/api">Baidu</option>
                            <option value="https://glm-llm-service.com/api">GLM</option>
                        </select>
                        <input id="apikey" type="text" placeholder="API Key (optional)">
                    </div>
                    <div class="options-sidebar second-options-sidebar">
                        <h2>感谢使用</h2>
                        <h2>欢迎联系：vx：547160794</h2>
                    </div>
                <!-- </div> -->
            </div>
        </div>
    </div>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    <script>
        document.addEventListener('DOMContentLoaded', (event) => {
            initEventSource();
        });
    </script>
</body>

</html>
```

