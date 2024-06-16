// static/js/main.js
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
}

// 随机生成用户ID的函数
function generateRandomUserId() {
    return Math.random().toString(36).substr(2, 9);
}

function getOrCreateUserId() {
    const storedUserId = localStorage.getItem('userId');
    if (!storedUserId) {
        const newUserId = generateRandomUserId();
        localStorage.setItem('userId', newUserId);
        return newUserId;
    }
    return storedUserId;
}

const userId = getOrCreateUserId();
document.getElementById('user_name').textContent = userId;

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
    messageDiv.classList.add('bot-bubble');
    if (isBot) {
        messageDiv.classList.add('bot-bubble');
    } else {
        messageDiv.classList.add('user-bubble');
    }
    console.log("sdfasdf", message)
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    // 滚动到底部
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const githubUrl = document.getElementById('github-url').value || null;
    const llmservice = document.getElementById('llmservice-select').value || 'glm';
    const apikey = document.getElementById('apikey').value || null;
    const seckey = document.getElementById('seckey').value || null;
    // const userId = document.getElementById('user_name').value || userId;
    console.log("userId",userId)

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
        seckey: seckey,
        github: githubUrl,
        userId: userId
    };

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => { // 返回的是一个数组的时候 用这个来解析
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
