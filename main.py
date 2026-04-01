import os, telebot, requests, threading
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Online"

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
bot = telebot.TeleBot(BOT_TOKEN)

def get_ai_response(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": text}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()
        if "candidates" in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            msg = res_json.get('error', {}).get('message', 'Noma'lum xato')
            return f"Google xatosi: {msg}"
    except Exception as e:
        return f"Ulanish xatosi: {str(e)}"

@bot.message_handler(func=lambda m: True)
def chat(m):
    javob = get_ai_response(m.text)
    bot.reply_to(m, javob)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()
    bot.infinity_polling()
    
