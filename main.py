
import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# Render o'chirib qo'ymasligi uchun kichik server
app = Flask(__name__)
@app.route('/')
def index():
    return "Bot is running!"

def run_server():
    # Render PORT muhit o'zgaruvchisini avtomatik beradi
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Bot va Gemini sozlamalari (Render'dagi Advanced bo'limidan o'qiydi)
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Foydalanuvchi yozgan matnni Gemini-ga yuboramiz
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Xatolik: {e}")
        bot.reply_to(message, "Hozircha javob bera olmayman, ozgina kutib turing.")

if __name__ == "__main__":
    # 1. Serverni alohida oqimda ishga tushirish
    threading.Thread(target=run_server).start()
    # 2. Botni ishga tushirish
    print("Bot ishga tushdi...")
    bot.infinity_polling()
  
