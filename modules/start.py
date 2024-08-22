from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from modules.database import is_allowed_user, save_user_string

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    if message.from_user.id in (OWNER_ID,) or is_allowed_user(message.from_user.id):
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Masukkan String", callback_data="enter_string")]
        ])
        await message.reply("Selamat datang! Klik tombol di bawah untuk memasukkan string.", reply_markup=buttons)
    else:
        await message.reply("Anda tidak memiliki izin untuk menggunakan bot ini.")

@app.on_callback_query(filters.regex("enter_string"))
async def on_enter_string(client, callback_query):
    if callback_query.from_user.id in (OWNER_ID,) or is_allowed_user(callback_query.from_user.id):
        await callback_query.message.reply("Silakan masukkan string Anda:")
        @app.on_message(filters.private & filters.incoming)
        async def save_string(client, message):
            save_user_string(callback_query.from_user.id, message.text)
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Tampilkan Pesan Dari Telegram", callback_data="show_messages")]
            ])
            await message.reply("String telah disimpan.", reply_markup=buttons)
    else:
        await callback_query.answer("Anda tidak diizinkan.", show_alert=True)
