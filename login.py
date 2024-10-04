import os
import asyncio
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded
import subprocess
import json

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

async def delete_selected_message(client, user_id, message_id):
    await client.delete_messages(user_id, message_id)
    print(f"Pesan dengan ID {message_id} telah dihapus.")

async def display_active_sessions(api_id, api_hash):
    try:
        async with PyrogramClient("my_account", api_id=api_id, api_hash=api_hash) as client:
            me = await client.get_me()
            print(f"Detail Akun: {me.first_name} {me.last_name} (@{me.username})")
            sessions = await client.get_sessions()
            for session in sessions:
                print(f"- Sesi: {session.device} di {session.platform}, aktif sejak {session.date}")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil sesi aktif: {e}")

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
                print("3. Hapus Pesan Terpilih Dari user id 777000")
                print("4. Update Repo")
                print("5. Beralih Akun")
                print("6. Detail Akun")
                print("7. Sesi Aktif")
                print("8. Keluar")
                choice = input("Pilih opsi (1/2/3/4/5/6/7/8): ")

                if choice == "1":
                    print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                    await fetch_latest_messages(app, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif choice == "3":
                    message_id = int(input("Masukkan ID pesan yang ingin dihapus: "))
                    await delete_selected_message(app, 777000, message_id)
                elif choice == "4":
                    print("Melakukan update repo...")
                    subprocess.call(["git", "pull"])
                    print("Repo berhasil diperbarui. Memulai ulang program...")
                    os.execv(__file__, ['python'] + sys.argv)  # Restart the script
                elif choice == "5":
                    break
                elif choice == "6":
                    print(f"Detail Akun: ID={me.id}, Username=@{me.username}, Nama={me.first_name} {me.last_name}, Nomor={phone_number}")
                elif choice == "7":
                    api_id = input("Masukkan API ID: ")
                    api_hash = input("Masukkan API Hash: ")
                    await display_active_sessions(api_id, api_hash)
                elif choice == "8":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

            remove_pid_file()
    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor. Silakan login secara manual untuk mendapatkan string sesi yang baru.")

async def main():
    check_if_running()

    print("Pilih opsi:")
    print("1. Login Baru")
    print("2. Login ke Akun Tersimpan")
    choice = input("Pilih opsi (1/2): ")

    if choice == "1":
        session_string = input("Masukkan string sesi Telegram (Pyrogram) Anda: ")
        await pyrogram_main(session_string)
    elif choice == "2":
        try:
            with open("saved_sessions.json") as f:
                sessions = json.load(f)
                print("Akun Tersimpan:")
                for idx, account in enumerate(sessions):
                    print(f"{idx + 1}. {account['username']}")
                selected_account = int(input("Pilih akun yang ingin login: ")) - 1
                session_string = sessions[selected_account]["session_string"]
                await pyrogram_main(session_string)
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
