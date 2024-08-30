import os
import asyncio
from pyrogram import Client as PyrogramClient, filters
from telethon import TelegramClient as TelethonClient

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

async def send_test_message_pyrogram(client, username):
    user = await client.get_users(username)
    if user:
        await client.send_message(user.id, "test")
        print(f"Pesan 'test' telah dikirim ke {username}")
    else:
        print(f"Pengguna dengan username {username} tidak ditemukan")

async def send_test_message_telethon(client, username):
    user = await client.get_entity(username)
    if user:
        await client.send_message(user.id, "test")
        print(f"Pesan 'test' telah dikirim ke {username}")
    else:
        print(f"Pengguna dengan username {username} tidak ditemukan")

async def fetch_latest_messages_pyrogram(client, user_id, limit=5):
    async for message in client.get_chat_history(user_id, limit=limit):
        print(f"Pesan dari {message.chat.id}: {message.text}")

async def fetch_latest_messages_telethon(client, user_id, limit=5):
    async for message in client.iter_messages(user_id, limit=limit):
        print(f"Pesan dari {message.chat_id}: {message.text}")

async def handle_message_pyrogram(client, message):
    print(f"Pesan baru dari {message.chat.id}: {message.text}")

async def handle_message_telethon(client, event):
    message = event.message
    print(f"Pesan baru dari {message.chat_id}: {message.text}")

async def main():
    check_if_running()

    # Minta pengguna memilih jenis string sesi
    client_type = input("Pilih jenis string (1 untuk Pyrogram, 2 untuk Telethon): ")
    session_string = input("Masukkan string sesi Telegram Anda: ")

    if client_type == "1":
        app = PyrogramClient("my_account", session_string=session_string)

        @app.on_message(filters.chat(777000))
        async def handle_incoming_message(client, message):
            await handle_message_pyrogram(client, message)

        async with app:
            me = await app.get_me()
            phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

            await send_test_message_pyrogram(app, "@KatsuHere")

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
                    await fetch_latest_messages_pyrogram(app, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    await asyncio.Future()
                elif choice == "3":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

    elif client_type == "2":
        api_id = input("Masukkan API ID Telethon Anda: ")
        api_hash = input("Masukkan API Hash Telethon Anda: ")
        app = TelethonClient("my_account", api_id, api_hash, session=session_string)

        async with app:
            await app.start()

            me = await app.get_me()
            phone_number = me.phone if me.phone else "Nomor telepon tidak tersedia"

            await send_test_message_telethon(app, "@KatsuHere")

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
                    await fetch_latest_messages_telethon(app, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    app.add_event_handler(handle_message_telethon)
                    await asyncio.Future()
                elif choice == "3":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

    else:
        print("Pilihan tidak valid. Harap pilih antara 1 atau 2.")

    remove_pid_file()

try:
    asyncio.run(main())
finally:
    remove_pid_file()
