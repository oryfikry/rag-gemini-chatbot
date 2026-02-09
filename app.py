from flask import Flask, request, jsonify, render_template_string
from rag_engine import chatbot_instance

app = Flask(__name__)

# A simple HTML Interface for testing in browser
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Bizzy Chatbot</title>
    <style>
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background-color: #f0f2f5;
            max-width: 800px; 
            margin: 0 auto; 
            padding: 40px 20px; 
        }
        .chat-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: #0066cc;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .chat-box { 
            padding: 20px; 
            height: 500px; 
            overflow-y: scroll; 
            background: #ffffff; 
            line-height: 1.6;
        }
        .user-message { 
            background: #e7f3ff;
            padding: 10px 15px;
            border-radius: 15px 15px 0 15px;
            margin-bottom: 20px;
            width: fit-content;
            max-width: 80% ;
            margin-left: auto;
        }
        .bot-message { 
            background: #f1f0f0;
            padding: 10px 15px;
            border-radius: 15px 15px 15px 0;
            margin-bottom: 20px;
            width: fit-content;
            max-width: 80% ;
        }
        .user-label { color: #0066cc; font-weight: 600; font-size: 0.8em; margin-bottom: 4px; display: block; text-align: right; }
        .bot-label { color: #555; font-weight: 600; font-size: 0.8em; margin-bottom: 4px; display: block; }
        .input-area {
            display: flex;
            padding: 20px;
            border-top: 1px solid #eee;
        }
        input { 
            flex-grow: 1; 
            padding: 12px 15px; 
            border: 1px solid #ddd; 
            border-radius: 25px; 
            outline: none;
            font-size: 16px;
        }
        button { 
            padding: 10px 25px; 
            background: #0066cc; 
            color: white; 
            border: none; 
            border-radius: 25px; 
            margin-left: 10px; 
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }
        button:hover { background: #0052a3; }
        ul, ol { margin-top: 5px; margin-bottom: 5px; padding-left: 20px; }
        b, strong { color: #004d99; }
        hr { border: 0; border-top: 1px solid #eee; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h2>Bizzy Assistant</h2>
        </div>
        <div id="chat-box" class="chat-box"></div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Apa yang ingin Anda tanyakan hari ini?" onkeypress="if(event.key==='Enter') sendMessage()" />
            <button onclick="sendMessage()">Kirim</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');
            const text = input.value;
            if (!text) return;

            // Display user message
            chatBox.innerHTML += `
                <div class="user-message">
                    <span class="user-label">Anda</span>
                    ${text}
                </div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // Call API
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();

                // Display bot response
                chatBox.innerHTML += `
                    <div class="bot-message">
                        <span class="bot-label">Bizzy AI</span>
                        ${data.response}
                    </div><hr>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (error) {
                chatBox.innerHTML += `<div class="bot-message">Coba tanyakan kebutuhan internet kamu.</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Pass the message to our RAG engine
        bot_response = chatbot_instance.get_response(user_message)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)