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

# 3. Gemini sozlash
genai.configure(api_key=GEMINI_KEY)

# BU YERDA MODELNI TO'G'RI TANLASH (Eng ishonchli usul)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        # Gemini-dan javob olish
        response = model.generate_content(m.text)
        bot.reply_to(m, response.text)
    except Exception as e:
        # Xato bo'lsa, modelni boshqa nom bilan qayta urinib ko'radi
        try:
            alt_model = genai.GenerativeModel('gemini-pro')
            response = alt_model.generate_content(m.text)
            bot.reply_to(m, response.text)
        except:
            bot.reply_to(m, f"Xato: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
