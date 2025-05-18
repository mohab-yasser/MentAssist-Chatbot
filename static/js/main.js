function sendMessage() {
    const input = document.getElementById('userInput');
    const text = input.value.trim();
    if (text !== '') {
        addMessage(text, 'user');
        setTimeout(() => {
            botReply(text);
        }, 800);
    }
    input.value = '';
}

function addMessage(text, sender) {
    const chat = document.getElementById('chat');
    const message = document.createElement('div');
    message.className = `message ${sender}`;

    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerText = text;

    message.appendChild(content);
    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
}

function botReply(userText) {
    showTyping();

    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userText })
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        hideTyping();
        const reply = data.reply || "I'm here to listen. Please, tell me more.";
        addMessage(reply, 'bot');
    })
    .catch(error => {
        hideTyping();
        console.error('Fetch error:', error);
        addMessage("Sorry, I couldn't connect to the assistant right now. Please try again later.", 'bot');
    });
}

function showTyping() {
    const chat = document.getElementById('chat');
    const typing = document.createElement('div');
    typing.id = 'typing-indicator';
    typing.className = 'message bot';
    typing.innerHTML = '<div class="message-content">Mental Assist is typing...</div>';
    chat.appendChild(typing);
    chat.scrollTop = chat.scrollHeight;
}

function hideTyping() {
    const typing = document.getElementById('typing-indicator');
    if (typing) {
        typing.remove();
    }
}

window.onload = function () {
    setTimeout(() => {
        addMessage("Welcome to Mental Assist 🌟 Feel free to share your thoughts.", 'bot');
    }, 500);

    // ✅ تأكد أن الزر موجود
    const sendBtn = document.getElementById('sendButton');
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    // ✅ إضافة دعم للضغط على Enter في الحقل
    const input = document.getElementById('userInput');
    if (input) {
        input.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
};
