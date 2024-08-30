import os
import asyncio
from pyrogram import Client, filters
from telethon import TelegramClient

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
    await client.send_message(username, "test")
    print(f"Pesan 'test' telah dikirim ke {username}")

async def fetch_latest_messages_pyrogram(client, user_id, limit=5):
    # Ambil pesan terbaru dari chat dengan user_id
    async for message in client.get_chat_history(user_id, limit=limit):
        print(f"Pesan dari {message.chat.id}: {message.text}")

async def fetch_latest_messages_telethon(client, user_id, limit=5):
    messages = await client.get_messages(user_id, limit=limit)
    for message in messages:
        print(f"Pesan dari {message.sender_id}: {message.text}")

async def main():
    check_if_running()

    # Memilih jenis client yang akan digunakan
    print("Pilih jenis string yang akan dimasukkan:")
    print("1. Pyrogram")
    print("2. Telethon")
    client_type = input("Masukkan pilihan Anda (1/2): ")

    if client_type == "1":
        # Pyrogram
        session_string = input("Masukkan string sesi Pyrogram Anda: ")
        app = Client("my_account", session_string=session_string)

        async with app:
            # Dapatkan informasi akun yang sedang login
            me = await app.get_me()

            # Coba dapatkan nomor telepon (jika tersedia)
            phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

            # Kirim pesan "test" ke pengguna dengan username @KatsuHere
            await send_test_message_pyrogram(app, "@KatsuHere")

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
                    await fetch_latest_messages_pyrogram(app, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    # Tunggu hingga program dihentikan atau pengguna memilih keluar
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif choice == "3":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")
                    
    elif client_type == "2":
        # Telethon
        session_string = input("Masukkan string sesi Telethon Anda: ")

        # Anda perlu memasukkan api_id dan api_hash di sini
        api_id = 123456  # Ganti dengan API ID Telegram Anda
        api_hash = 'your_api_hash_here'  # Ganti dengan API Hash Telegram Anda

        # Buat klien menggunakan string sesi
        client = TelegramClient("anon", api_id, api_hash)
        client = await client.start(bot_token=None, phone=None, password=None, force_sms=False, code_callback=None, email_code_callback=None, qr_code_callback=None, password_callback=None, string=session_string)

        async with client:
            # Dapatkan informasi akun yang sedang login
            me = await client.get_me()

            # Kirim pesan "test" ke pengguna dengan username @KatsuHere
            await send_test_message_telethon(client, "@KatsuHere")

            # Tampilkan detail akun
            print(f"ID: {me.id}")
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
                    await fetch_latest_messages_telethon(client, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    # Tunggu hingga program dihentikan atau pengguna memilih keluar
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif choice == "3":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")
                    
    else:
        print("Pilihan tidak valid. Program dihentikan.")
        return

    # Menghentikan program setelah selesai
    remove_pid_file()

try:
    asyncio.run(main())
finally:
    remove_pid_file()
