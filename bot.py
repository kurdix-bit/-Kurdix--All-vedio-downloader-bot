import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests

# هذا هو التوكن الخاص بك:
TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()

# نصوص الرسائل بمختلف اللغات
MESSAGES = {
    "ar": "أرسل رابط الفيديو للتحميل 📥",
    "de": "Senden Sie den Video-Link zum Herunterladen 📥",
    "en": "Send the video link to download 📥",
    "ku_so": "لینکی ڤیدیۆکە بنێرە بۆ دابەزاندن 📥",
    "ku_la": "Lînka vîdyoyê bişîne ji bo daxistinê 📥"
}

# دالة إنشاء قائمة اللغات
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
    url = message.text
    if not url.startswith("http"): return

    lang = user_langs.get(message.from_user.id, "en")
    wait_text = "Wait..." if lang == "en" else "چاوەڕێ بکە..." if "ku" in lang else "انتظر..."
    status_msg = await message.answer(wait_text)

    try:
        # استخدام API لتحميل الفيديو بشكل أسرع وأخف على الخادم
        api_url = f"https://api.onlinevideoconverter.pro{url}"
        response = requests.get(api_url).json()

        if response.get("status") == "ok":
            video_url = response.get("download_url")
            await bot.send_video(message.chat.id, video_url, caption="تم التحميل بنجاح ✅")
        else:
            await message.answer(f"❌ حدث خطأ في معالجة الرابط: {response.get('message', 'غير معروف')}")
            
    except Exception as e:
        await message.answer(f"❌ حدث خطأ غير متوقع: {str(e)}")
    finally:
        await status_msg.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    await message.answer("Please choose your language / تکایە زمانەکەت هەڵبژێرە / اختر لغتك:", reply_markup=get_lang_keyboard())

@dp.callback_query(F.data.startswith("set_"))
async def set_language(callback: types.CallbackQuery):
    lang_code = callback.data.replace("set_", "")
    user_langs[callback.from_user.id] = lang_code
    await callback.message.edit_text(MESSAGES[lang_code])

@dp.message()
async def download_video(message: types.Message):
    url = message.text
    if not url.startswith("http"): return

    lang = user_langs.get(message.from_user.id, "en")
    wait_text = "Wait..." if lang == "en" else "چاوەڕێ بکە..." if "ku" in lang else "انتظر..."
    status_msg = await message.answer(wait_text)

    try:
        # استخدام API لتحميل الفيديو بشكل أسرع وأخف على الخادم
        api_url = f"api.onlinevideoconverter.pro{url}"
        response = requests.get(api_url).json()

        if response.get("status") == "ok":
            video_url = response.get("download_url")
            await bot.send_video(message.chat.id, video_url, caption="تم التحميل بنجاح ✅")
        else:
            await message.answer(f"❌ حدث خطأ في معالجة الرابط: {response.get('message', 'غير معروف')}")
            
    except Exception as e:
        await message.answer(f"❌ حدث خطأ غير متوقع: {str(e)}")
    finally:
        await status_msg.delete()

async def main():
    # تأكد من أن التوكن موضوع هنا قبل التشغيل
    if TOKEN == "ضع_التوكن_الخاص_بك_هنا":
        print("الرجاء وضع التوكن في الكود قبل التشغيل!")
    else:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
