import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import yt_dlp

# ضع هنا التوكن الذي حصلت عليه من BotFather
TOKEN = "ضع_التوكن_الخاص_بك_هنا"

bot = Bot(token=TOKEN)
dp = Dispatcher()

MESSAGES = {
    "ar": "أرسل رابط الفيديو للتحميل 📥",
    "de": "Senden Sie den Video-Link zum Herunterladen 📥",
    "en": "Send the video link to download 📥",
    "ku_so": "لینکی ڤیدیۆکە بنێرە بۆ دابەزاندن 📥",
    "ku_la": "Lînka vîdyoyê bişîne ji bo daxistinê 📥"
}

def get_lang_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="العربية 🇸🇦", callback_data="set_ar"))
    builder.row(types.InlineKeyboardButton(text="Deutsch 🇩🇪", callback_data="set_de"))
    builder.row(types.InlineKeyboardButton(text="English 🇺🇸", callback_data="set_en"))
    builder.row(types.InlineKeyboardButton(text="Kurdî (Soranî) ☀️", callback_data="set_ku_so"))
    builder.row(types.InlineKeyboardButton(text="Kurdî (Latînî) ☀️", callback_data="set_ku_la"))
    return builder.as_markup()

user_langs = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Please choose your language / تکایە زمانەکەت هەڵبژێرە / اختر لغتك:", reply_markup=get_lang_keyboard())

@dp.callback_query(F.data.startswith("set_"))
async def set_language(callback: types.CallbackQuery):
    lang_code = callback.data.replace("set_", "")
    user_langs[callback.from_user.id] = lang_code
    await callback.message.edit_text(MESSAGES[lang_code])

@dp.message()
async def download_video(message: types.Message):
    if not message.text.startswith("http"): return
    
    lang = user_langs.get(message.from_user.id, "en")
    wait_text = "Wait..." if lang == "en" else "چاوەڕێ بکە..." if "ku" in lang else "انتظر..."
    status = await message.answer(wait_text)
    
    file_path = f"{message.chat.id}.mp4"
    ydl_opts = {'format': 'best[ext=mp4]/best', 'outtmpl': file_path, 'noplaylist': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        await bot.send_video(message.chat.id, types.FSInputFile(file_path))
        if os.path.exists(file_path): os.remove(file_path)
    except Exception as e:
        await message.answer(f"Error: {str(e)}")
    finally:
        await status.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

