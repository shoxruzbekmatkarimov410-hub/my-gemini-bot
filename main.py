import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# 1. Flask server (Render o'chib qolmasligi uchun)
app = Flask(__name__)
@app.route('/')
def index(): return "Bot holati: OK"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# 2. Kalitlarni olish
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# 3. Gemini sozlash (Model nomini 'gemini-pro' qildik - bu aniq ishlaydi!)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        # Gemini-dan javob olish
        response = model.generate_content(m.text)
        bot.reply_to(m, response.text)
    except Exception as e:
        # Xatoni Telegramga yuborish (nima bo'layotganini bilish uchun)
        bot.reply_to(m, f"Xato turi: {str(e)}")

if __name__ == "__main__":
    # Serverni alohida oqimda yurgizish
    threading.Thread(target=run_flask).start()
    # Botni ishga tushirish
    bot.infinity_polling()
                                          
