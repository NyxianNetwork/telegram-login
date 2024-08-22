from pyrogram import filters
from modules.database import add_permission, remove_permission, add_sudo, remove_sudo

@app.on_message(filters.command(["izin", "hapusizin", "addsudo", "delsudo"]) & filters.user(OWNER_ID))
async def izin_handler(client, message):
    command = message.command[0]
    user_id = int(message.command[1])

    if command == "izin":
        days = int(message.command[2])
        add_permission(user_id, days)
        await message.reply(f"Pengguna {user_id} telah diberikan izin selama {days} hari.")
    elif command == "hapusizin":
        remove_permission(user_id)
        await message.reply(f"Izin pengguna {user_id} telah dicabut.")
    elif command == "addsudo":
        add_sudo(user_id)
        await message.reply(f"Pengguna {user_id} telah ditambahkan sebagai Sudo.")
    elif command == "delsudo":
        remove_sudo(user_id)
        await message.reply(f"Pengguna {user_id} telah dihapus dari Sudo.")
