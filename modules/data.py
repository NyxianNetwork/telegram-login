from pyrogram import filters
from modules.database import get_user_string
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_callback_query(filters.regex("show_messages"))
async def show_messages(client, callback_query):
    if callback_query.from_user.id in (OWNER_ID,) or is_allowed_user(callback_query.from_user.id):
        # Ambil dan tampilkan 5 pesan terakhir dari user id 777000
        messages = await fetch_latest_messages(client, 777000)
        for msg in messages:
            await callback_query.message.reply(msg)
    else:
        await callback_query.answer("Anda tidak diizinkan.", show_alert=True)
