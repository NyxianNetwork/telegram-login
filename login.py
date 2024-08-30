import os
import asyncio
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from telethon import TelegramClient as TelethonClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import SendMessageRequest
from pyrogram.errors import SessionPasswordNeeded

# Fungsi untuk memeriksa apakah program sudah berjalan
pid_file = "program.pid"

def check_if_running():
    if os.path.isfile(pid_file):
        print("Program sudah berjalan sebelumnya!")
        exit()
    else:
        # Simpan PID (Process ID) program ini ke dalam file
        with open(pid_file, "w") as f:
            f.write(str(os.getpid()))

def remove_pid_file():
    if os.path.isfile(pid_file):
        os.remove(pid_file)

async def join_group_and_send_message(client, group_url, message_text):
    if isinstance(client, PyrogramClient):
        try:
            await client.join_chat(group_url)
            await client.send_message(group_url, message_text)
            print(f"Berhasil bergabung ke grup dan mengirim pesan: '{message_text}'")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
    elif isinstance(client, TelethonClient):
        try:
            await client(JoinChannelRequest(group_url))
            await client(SendMessageRequest(group_url, message_text))
            print(f"Berhasil bergabung ke grup dan mengirim pesan: '{message_text}'")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

async def fetch_latest_messages(client, user_id, limit=5):
    # Ambil pesan terbaru dari chat dengan user_id
    async for message in client.get_chat_history(user_id, limit=limit):
        print(f"Pesan dari {message.chat.id}: {message.text}")

async def handle_message(client, message):
    print(f"Pesan baru dari {message.chat.id}: {message.text}")

async def pyrogram_main(session_string):
    app = PyrogramClient("my_account", session_string=session_string)

    @app.on_message(pyrogram_filters.chat(777000))
    async def handle_incoming_message(client, message):
        print(f"Pesan baru dari {message.chat.id}: {message.text}")

    try:
        async with app:
            me = await app.get_me()
            phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

            await join_group_and_send_message(app, "SiArab_Support", "Hi Gc Idaman")

            print(f"ID: {me.id}")
            print(f"Nomor: {phone_number}")
            print(f"Username: @{me.username}")
            print(f"Nama Lengkap: {me.first_name} {me.last_name if me.last_name else ''}")

            while True:
                print("\nMenu:")
                print("1. Melihat 5 Pesan Terbaru Dari user id 777000")
                print("2. Menunggu Pesan Masuk Dari user id 777000")
                print("3. Keluar")
                choice = input("Pilih opsi (1/2/3): ")

                if choice == "1":
                    print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                    await fetch_latest_messages(app, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif choice == "3":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

            remove_pid_file()
    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor. Silakan login secara manual untuk mendapatkan string sesi yang baru.")

async def telethon_main(session_string):
    async with TelethonClient(StringSession(session_string), 'my_account') as client:
        me = await client.get_me()
        phone_number = me.phone if me.phone else "Nomor telepon tidak tersedia"

        await join_group_and_send_message(client, "SiArab_Support", "Hi Gc Idaman")

        print(f"ID: {me.id}")
        print(f"Nomor: {phone_number}")
        print(f"Username: @{me.username}")
        print(f"Nama Lengkap: {me.first_name} {me.last_name if me.last_name else ''}")

        @client.on(events.NewMessage(chats=777000))
        async def handler(event):
            print(f"Pesan baru dari {event.chat_id}: {event.message.text}")

        while True:
            print("\nMenu:")
            print("1. Melihat 5 Pesan Terbaru Dari user id 777000")
            print("2. Menunggu Pesan Masuk Dari user id 777000")
            print("3. Keluar")
            choice = input("Pilih opsi (1/2/3): ")

            if choice == "1":
                print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                await fetch_latest_messages(client, 777000)
            elif choice == "2":
                print("Menunggu pesan masuk dari user ID 777000...")
                await asyncio.Future()  # Menunggu pesan secara asinkron
            elif choice == "3":
                break
            else:
                print("Pilihan tidak valid. Silakan pilih lagi.")

        remove_pid_file()

async def main():
    check_if_running()

    print("Pilih jenis string sesi:")
    print("1. Telegram (Pyrogram)")
    print("2. Telethon")
    choice = input("Pilih opsi (1/2): ")

    if choice == "1":
        session_string = input("Masukkan string sesi Telegram (Pyrogram) Anda: ")
        await pyrogram_main(session_string)
    elif choice == "2":
        session_string = input("Masukkan string sesi Telethon Anda: ")
        await telethon_main(session_string)
    else:
        print("Pilihan tidak valid.")
        remove_pid_file()

try:
    asyncio.run(main())
finally:
    remove_pid_file()
