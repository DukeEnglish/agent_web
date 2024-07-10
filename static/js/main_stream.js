// document.addEventListener('DOMContentLoaded', initEventSource);
let eventSource = null;
let currentMessageDiv; // 当前消息 div
let fullMessage = ''; // 用于存储拼接的所有消息
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



function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const githubUrl = document.getElementById('github-url').value || null;
    const llmservice = document.getElementById('llmservice-select').value || 'ernie';
    const apikey = document.getElementById('apikey').value || null;
    const seckey = document.getElementById('seckey').value || null;
    const user_id = document.getElementById('user_name').value || userId;

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
        userId: user_id
    };

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => { // 返回的是一个数组的时候 用这个来解析
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        if (!eventSource) {
            initEventSource();
        }
        return response.json();
    })
    
    .catch(error => console.error('Error:', error));
    document.getElementById('user-input').value = '';
}

// 新写的函数，用于初始化和监听 SSE（Server-Sent Events）
function initEventSource() {
    const eventSource = new EventSource('/chat');

    eventSource.onmessage = function(event) {
        // 解析 JSON 数据
        // console.log(event.data)
        if (event){
        const messageObj = JSON.parse(event.data);
        // console.log(messageObj)
        if (messageObj.isComplete != null) {
        addMessageToChatHistory(messageObj.botMessage, true, messageObj.isComplete);}
    }};

    eventSource.onerror = function(event) {
        console.error('EventSource failed:', event);
        eventSource.close();
    };
}
/* 新写的函数，用于添加消息到聊天历史 */
function addMessageToChatHistory(message, isBot, isComplete) {
    
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
    
    if (fullMessage) {
        chatBox.removeChild(chatBox.lastChild)
    }
    fullMessage += message; // 拼接所有消息
        // const messageDiv = document.createElement('div');
        // messageDiv.classList.add('bot-message');
    messageDiv.innerHTML += marked.parse(fullMessage);
    // fullMessage = ''
    // chatBox.innerHTML = ''; // 清空之前的内容
        // chatBox.appendChild(messageDiv);
    console.log("123",message, isComplete)
    if (isComplete) {
        console.log("123",message)
        fullMessage = ''
    }
    chatBox.appendChild(messageDiv);
    // 滚动到底部
    chatBox.scrollTop = chatBox.scrollHeight;
}

function clearChatHistory() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
}
