import os
import asyncio
from pyrogram import Client as PyrogramClient, filters
from telethon import TelegramClient as TelethonClient
from telethon.tl.functions.messages import GetHistoryRequest

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
    if isinstance(client, PyrogramClient):
        user = await client.get_users(username)
        if user:
            await client.send_message(user.id, "test")
            print(f"Pesan 'test' telah dikirim ke {username}")
        else:
            print(f"Pengguna dengan username {username} tidak ditemukan")
    elif isinstance(client, TelethonClient):
        user = await client.get_entity(username)
        if user:
            await client.send_message(user.id, "test")
            print(f"Pesan 'test' telah dikirim ke {username}")
        else:
            print(f"Pengguna dengan username {username} tidak ditemukan")

async def fetch_latest_messages(client, user_id, limit=5):
    if isinstance(client, PyrogramClient):
        async for message in client.get_chat_history(user_id, limit=limit):
            print(f"Pesan dari {message.chat.id}: {message.text}")
    elif isinstance(client, TelethonClient):
        history = await client(GetHistoryRequest(peer=user_id, limit=limit))
        for message in history.messages:
            print(f"Pesan dari {message.chat_id}: {message.text}")

async def handle_message(client, message):
    print(f"Pesan baru dari {message.chat.id}: {message.text}")

async def main():
    check_if_running()

    # Pilihan jenis string sesi
    client_type = input("Pilih jenis client (1 untuk Pyrogram, 2 untuk Telethon): ")
    session_string = input("Masukkan string sesi Telegram Anda: ")

    if client_type == "1":
        app = PyrogramClient("my_account", session_string=session_string)
        message_filter = filters.chat(777000)
    elif client_type == "2":
        app = TelethonClient("my_account", session_string=session_string)
        message_filter = None
    else:
        print("Jenis client tidak valid!")
        return

    async with app:
        # Dapatkan informasi akun yang sedang login
        if client_type == "1":
            me = await app.get_me()
            phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"
        elif client_type == "2":
            me = await app.get_me()
            phone_number = me.phone if me.phone else "Nomor telepon tidak tersedia"

        # Kirim pesan "test" ke pengguna dengan username @KatsuHere
        await send_test_message(app, "@KatsuHere")

        # Tampilkan detail akun
        print(f"ID: {me.id}")
        print(f"Nomor: {phone_number}")
        print(f"Username: @{me.username}")
        print(f"Nama Lengkap: {me.first_name} {me.last_name if me.last_name else ''}")

        # Menu pilihan
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
                # Tunggu hingga program dihentikan atau pengguna memilih keluar
                if client_type == "1":
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif client_type == "2":
                    # Telethon tidak memiliki metode built-in untuk menunggu pesan seperti Pyrogram
                    await app.run_until_disconnected()
            elif choice == "3":
                break
            else:
                print("Pilihan tidak valid. Silakan pilih lagi.")

        # Menghentikan program setelah selesai
        remove_pid_file()

try:
    asyncio.run(main())
finally:
    remove_pid_file()
