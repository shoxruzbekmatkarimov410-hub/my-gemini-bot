import os, telebot, google.generativeai as genai
from flask import Flask
import threading

# 1. Oddiy server (Render o'chib qolmasligi uchun)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot ishlayapti!"

# 2. Gemini va Botni sozlash
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

genai.configure(api_key=GEMINI_KEY)
# Eng asosiysi - model nomi mana shunday bo'lishi kerak:
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# 3. Xabarlarga javob berish qismi
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xato: {str(e)}")

# 4. Botni yurgizish
if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))).start()
    bot.infinity_polling()
