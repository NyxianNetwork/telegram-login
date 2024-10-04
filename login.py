import os
import asyncio
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
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
    try:
        await client.join_chat(group_url)
        await client.send_message(group_url, message_text)
        print(f"Berhasil bergabung ke grup dan mengirim pesan: '{message_text}'")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

async def fetch_latest_messages(client, user_id, limit=5):
    # Ambil pesan terbaru dari chat dengan user_id
    async for message in client.get_chat_history(user_id, limit=limit):
        print(f"Pesan ID {message.message_id} dari {message.chat.id}: {message.text}")

async def delete_last_message(client, user_id):
    # Ambil satu pesan terbaru dari chat dengan user_id
    async for message in client.get_chat_history(user_id, limit=1):
        await client.delete_messages(user_id, message.message_id)
        print(f"Pesan dengan ID {message.message_id} telah dihapus.")

async def display_active_sessions(api_id, api_hash, session_string):
    async with PyrogramClient("active_sessions", api_id=api_id, api_hash=api_hash, session_string=session_string) as client:
        me = await client.get_me()
        print(f"Informasi sesi aktif untuk: {me.first_name} @{me.username}")
        sessions = await client.get_active_sessions()
        for session in sessions:
            print(f"Device: {session.device}, Platform: {session.platform}, Last Seen: {session.last_seen}")

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
                print("3. Hapus 1 Pesan dari user id 777000")
                print("4. Sesi Aktif")
                print("5. Keluar")
                choice = input("Pilih opsi (1/2/3/4/5): ")

                if choice == "1":
                    print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                    await fetch_latest_messages(app, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif choice == "3":
                    print("Menghapus 1 pesan terbaru dari user ID 777000...")
                    await delete_last_message(app, 777000)
                elif choice == "4":
                    api_id = input("Masukkan API ID Anda: ")
                    api_hash = input("Masukkan API Hash Anda: ")
                    await display_active_sessions(api_id, api_hash, session_string)
                elif choice == "5":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

            remove_pid_file()
    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor. Silakan login secara manual untuk mendapatkan string sesi yang baru.")

async def main():
    check_if_running()

    session_string = input("Masukkan string sesi Telegram (Pyrogram) Anda: ")
    await pyrogram_main(session_string)

try:
    asyncio.run(main())
finally:
    remove_pid_file()
