import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# Flask server (Render uchun)
app = Flask(__name__)
@app.route('/')
def index(): return "Bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Kalitlarni olish
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Gemini sozlash
genai.configure(api_key=GEMINI_KEY)
# MUHIM: Model nomini 'gemini-1.5-flash' ga o'zgartirdik
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        # Xabarni yuborish
        response = model.generate_content(m.text)
        bot.reply_to(m, response.text)
    except Exception as e:
        # Xatoni aniq Telegramga yuborish (shunda nima bo'layotganini bilamiz)
        error_message = str(e)
        bot.reply_to(m, f"Xato turi: {error_message}")
        print(f"LOG XATO: {error_message}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
        
