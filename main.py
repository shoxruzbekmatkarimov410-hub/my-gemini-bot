import os, telebot, requests, threading
from flask import Flask

# 1. Server qismi
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Active"

# 2. Sozlamalar
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
bot = telebot.TeleBot(BOT_TOKEN)

# 3. Gemini bilan to'g'ridan-to'g'ri bog'lanish (Kutubxonasiz)
def get_ai_response(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": text}]}]}
    
    response = requests.post(url, headers=headers, json=data)
    res_json = response.json()
    
    if "candidates" in res_json:
        return res_json['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Xato chiqdi: {res_json}"

# 4. Telegram xabarlari
@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        javob = get_ai_response(m.text)
        bot.reply_to(m, javob)
    except Exception as e:
        bot.reply_to(m, "Ulanishda muammo bo'ldi.")

# 5. Ishga tushirish
if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))).start()
    bot.infinity_polling()
    
