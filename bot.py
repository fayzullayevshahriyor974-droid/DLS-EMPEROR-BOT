import logging
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Render uchun kichik veb-server (port talabini bajarish uchun)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_check_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Veb-serverni fonda ishga tushiramiz
Thread(target=run_health_check_server, daemon=True).start()

# --- BOT SOZLAMALARI ---
API_TOKEN = '9236095419:AAHHi81bV8pPQcOdqQptRVYUAQfgf7idDuE'
CHANNEL_USERNAME = '@dls_emperor'
GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfqSu1sBIVmTt4CLbXQMnIu3FNDJ15ZwFsp3zgG'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['creator', 'administrator', 'member']
    except Exception:
        return False

# Agar botingizda boshqa handlerlar bo'lsa, ularni shu yerga qo'shasiz.

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
