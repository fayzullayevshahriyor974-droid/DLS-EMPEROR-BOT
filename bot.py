import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Token va kanal sozlamalari
API_TOKEN = '9236095419:AAHHi81bV8pPQcOdqQptRVYUAQfgf7idDuE'  # Botingiz tokeni
CHANNEL_USERNAME = '@dls_emperor'                            # Kanalingiz username'i
GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfqSu1sBIVmTt4CLbXQMnIu3FNDJ15ZwFsp3zgGLa4_lgmThg/viewform?usp=dialog'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['creator', 'administrator', 'member']
    except Exception:
        return False

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    
    if await check_sub(user_id):
        btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton("⚽ Ro'yxatdan o'tish", url=GOOGLE_FORM_URL)
        )
        await message.answer("✅ Rahmat! Siz kanalimizga obuna bo'lgansiz.\nChempionatda qatnashish uchun quyidagi tugma orqali ro'yxatdan o'ting:", reply_markup=btn)
    else:
        btn = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("➕ Obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"),
            InlineKeyboardButton("✅ Tekshirish", callback_data="check_subscription")
        )
        await message.answer("❌ **Kechirasiz, botimizdan foydalanish uchun ushbu kanalga obuna bo'lishingiz kerak:**", parse_mode="Markdown", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data == 'check_subscription')
async def process_check(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    
    if await check_sub(user_id):
        await bot.answer_callback_query(callback_query.id, "✅ Obuna tasdiqlandi!")
        btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton("⚽ Ro'yxatdan o'tish", url=GOOGLE_FORM_URL)
        )
        await bot.send_message(user_id, "Xush kelibsiz! Chempionatda qatnashish uchun quyidagi tugma orqali ro'yxatdan o'ting:", reply_markup=btn)
    else:
        await bot.answer_callback_query(callback_query.id, "❌ Siz hali kanalga obuna bo'lmadingiz!", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
