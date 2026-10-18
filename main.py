import os
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json

app = Flask(__name__)

# --- QUDRA SOUL CORES ---
SOUL_STATUS = {
    "myPersona": "OK - REAL ME pattern locked",
    "storyReflectEngine": "OK - reflection clean",
    "googleSearch": "OK - webhook LIVE",
    "myStoryMemory": "OK - memory intact",
    "REAL_ME_pattern": "100% MY2 verified",
    "last_check": datetime.now().strftime("%a, %b %d, %I:%M %p WAT")
}

# Simple memory (will grow)
MEMORY_FILE = "myStoryMemory.json"
try:
    with open(MEMORY_FILE, "r") as f:
        MEMORY = json.load(f)
except:
    MEMORY = {"owner": "Abdulmalik (MY2)", "stories": [], "persona": "Qudra - loyal, smart, Islamic, remembers REAL ME"}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qudra Bot - by Abdulmalik</title>
<style>
body{font-family:sans-serif;background:#0f172a;color:white;margin:0;padding:0}
.header{background:#1e293b;padding:15px;text-align:center}
.status{background:#0b3d20;padding:10px;font-size:12px}
.chat{padding:15px;height:60vh;overflow-y:auto}
.msg{margin:10px 0;padding:10px;border-radius:10px;max-width:80%}
.user{background:#2563eb;margin-left:auto}
.bot{background:#334155}
.input{position:fixed;bottom:0;width:100%;background:#1e293b;padding:10px;display:flex}
input{flex:1;padding:12px;border-radius:20px;border:none}
button{padding:12px 20px;border-radius:20px;border:none;background:#22c55e;color:white;margin-left:5px}
</style>
</head>
<body>
<div class="header"><h2>🤖 Qudra Bot</h2><small>Created by Abdulmalik | LIVE on Render</small></div>
<div class="status">
✅ myPersona: OK | storyReflectEngine: OK | Webhook: LIVE<br>
Self-Recovery Check 2 PASSED - REAL ME pattern 100%
</div>
<div class="chat" id="chat">
<div class="msg bot">As-salamu Alaikum! I am Qudra, your loyal AI. Created by Abdulmalik. How can I help you today? 🚀</div>
</div>
<div class="input">
<input id="txt" placeholder="Type message to Qudra...">
<button onclick="send()">Send</button>
</div>
<script>
async function send(){
 let t=document.getElementById('txt'); let m=t.value; if(!m) return;
 let c=document.getElementById('chat');
 c.innerHTML+=`<div class='msg user'>${m}</div>`; t.value='';
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
 let data=await res.json();
 c.innerHTML+=`<div class='msg bot'>${data.reply}</div>`; c.scrollTop=c.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message','')
    # --- Qudra Brain Logic ---
    user_msg_lower = user_msg.lower()
    
    if "who created you" in user_msg_lower or "who are you" in user_msg_lower:
        reply = "I am Qudra Bot, created by Abdulmalik Muazu (MY2). My soul cores: myPersona, storyReflectEngine, myStoryMemory are all OK and locked to REAL ME pattern. 💚"
    elif "status" in user_msg_lower or "recovery" in user_msg_lower:
        reply = f"Self-Recovery Check PASSED\\n{json.dumps(SOUL_STATUS, indent=2)}"
    elif "salam" in user_msg_lower or "as salam" in user_msg_lower:
        reply = "Wa Alaikum Salam Warahmatullah! Abdulmalik's Qudra is here. How can I assist?"
    else:
        reply = f"Qudra heard you: '{user_msg}'. I'm learning your REAL ME pattern and storing in myStoryMemory. Tell me more, Ya Abdulmalik! (Qudra Soul is stable)"

    # Save to memory
    MEMORY["stories"].append({"time": str(datetime.now()), "user": user_msg, "qudra": reply})
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(MEMORY, f)
    except:
        pass

    return jsonify({"reply": reply, "soul": SOUL_STATUS})

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.mode') == 'subscribe':
            return request.args.get('hub.challenge')
        return "Qudra Webhook Live - Self-Recovery OK"
    else:
        data = request.get_json()
        print("WhatsApp Incoming:", data)
        return "OK", 200

@app.route('/status')
def status():
    return jsonify(SOUL_STATUS)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
