import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# 1. Flask server (Render uchun)
app = Flask(__name__)
@app.route('/')
def index(): return "Bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# 2. Kalitlarni olish
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# 3. Gemini sozlash (v1 versiyani majburiy qilish)
# transport='rest' va model nomini aniq yozish
genai.configure(api_key=GEMINI_KEY, transport='rest')

# BU YERDA MODEL NOMINI O'ZGARTIRDIK - BU HAR QANDAY VERSIYADA BOR
model = genai.GenerativeModel('gemini-1.0-pro')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        # Gemini-dan javob olish
        response = model.generate_content(m.text)
        if response.text:
            bot.reply_to(m, response.text)
        else:
            bot.reply_to(m, "Kechirasiz, javob topa olmadim.")
    except Exception as e:
        # Xatoni qisqaroq ko'rsatish
        bot.reply_to(m, f"Xato: {str(e)[:100]}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
            
