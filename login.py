import os
import asyncio
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded, FloodWait, PeerIdInvalid
from pyrogram.types import Chat
import time

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

async def join_group_and_send_message(client, invite_link, message):
    try:
        # Bergabung ke grup menggunakan tautan undangan
        await client.join_chat(invite_link)
        print(f"Berhasil bergabung ke grup dengan tautan: {invite_link}")

        # Mengirim pesan ke grup tersebut
        chat = await client.get_chat(invite_link)  # Mendapatkan informasi grup
        await client.send_message(chat.id, message)
        print(f"Pesan '{message}' telah dikirim ke grup: {chat.title}")
    except PeerIdInvalid:
        print("Tautan undangan grup tidak valid atau grup tidak dapat diakses.")
    except FloodWait as e:
        print(f"Perlu menunggu {e.x} detik sebelum melanjutkan.")
        time.sleep(e.x)
    except Exception as e:
        print(f"Gagal bergabung atau mengirim pesan: {e}")

async def fetch_latest_messages(client, user_id, limit=5):
    # Ambil pesan terbaru dari chat dengan user_id
    async for message in client.get_chat_history(user_id, limit=limit):
        print(f"Pesan dari {message.chat.id}: {message.text}")

async def pyrogram_main(session_string):
    app = PyrogramClient("my_account", session_string=session_string)

    @app.on_message(pyrogram_filters.chat(777000))
    async def handle_incoming_message(client, message):
        print(f"Pesan baru dari {message.chat.id}: {message.text}")

    try:
        async with app:
            me = await app.get_me()
            phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

            invite_link = "https://t.me/SiArab_Support"  # Tautan undangan grup
            await join_group_and_send_message(app, invite_link, "Hi")

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
                    print("Fitur ini hanya tersedia di Pyrogram versi terbaru. Harap gunakan Pyrogram untuk mengeluarkan sesi lain.")
                elif choice == "4":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

            remove_pid_file()
    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor. Silakan login secara manual untuk mendapatkan string sesi yang baru.")

async def main():
    check_if_running()

    print("Pilih jenis string sesi:")
    print("1. Telegram (Pyrogram)")
    choice = input("Pilih opsi (1): ")

    if choice == "1":
        session_string = input("Masukkan string sesi Telegram (Pyrogram) Anda: ")
        await pyrogram_main(session_string)
    else:
        print("Pilihan tidak valid.")
        remove_pid_file()

try:
    asyncio.run(main())
finally:
    remove_pid_file()
