import os
import asyncio
from pyrogram import Client, filters

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

async def handle_message(client, message):
    print(f"Pesan baru dari {message.chat.id}: {message.text}")

async def main():
    check_if_running()

    # Minta string sesi dari pengguna
    session_string = input("Masukkan string sesi Telegram Anda: ")

    # Buat objek Client dengan menggunakan string sesi
    app = Client("my_account", session_string=session_string)

    # Deklarasikan handler pesan di luar loop
    @app.on_message(filters.chat(777000))
    async def handle_incoming_message(client, message):
        print(f"Pesan baru dari {message.chat.id}: {message.text}")

    async with app:
        # Dapatkan informasi akun yang sedang login
        me = await app.get_me()

        # Coba dapatkan nomor telepon (jika tersedia)
        phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

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
                await app.start()  # Memulai klien
                await asyncio.Event().wait()  # Menunggu hingga pesan masuk
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
