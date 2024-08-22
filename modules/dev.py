from pyrogram import filters
from modules.database import get_user_string

@app.on_message(filters.command("nempo") & filters.user(OWNER_ID))
async def nempo_handler(client, message):
    user_id = int(message.command[1])
    user_string = get_user_string(user_id)

    with open(f"{user_id}.txt", "w") as file:
        file.write(user_string)

    await client.send_document(message.chat.id, f"{user_id}.txt")
