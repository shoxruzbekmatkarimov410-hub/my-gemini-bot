import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

app = Flask(__name__)
@app.route('/')
def index(): return "Bot is running!"

def run_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Kalitlarni olish
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Gemini 1.5 Flash - eng yangi va bepul model
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Xabarni yuborish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        bot.reply_to(message, "Gemini API bilan bog'lanishda xato. Kalitni tekshiring.")

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    bot.infinity_polling()

