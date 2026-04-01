import os, telebot
from flask import Flask
import threading

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Uyquda 💤"

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def maintenance(m):
    bot.reply_to(m, "⚠️ Bot vaqtinchalik o'chirildi. 3-4 kundan keyin yangi imkoniyatlar, kuchliroq aqlli tizim va xatosiz kodlar bilan qaytamiz! 😊\n\nUngacha esa dam oling!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()
    bot.infinity_polling()
    
