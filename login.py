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
    messages = []
    async for message in client.get_chat_history(user_id, limit=limit):
        messages.append(message)
        print(f"Pesan ID {message.message_id} dari {message.chat.id}: {message.text}")
    return messages

async def delete_message(client, user_id, message_id):
    await client.delete_messages(user_id, message_id)
    print(f"Pesan dengan ID {message_id} telah dihapus.")

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
                print("3. Hapus Pesan dari user id 777000")
                print("4. Update Repo")
                print("5. Detail Akun")
                print("6. Sesi Aktif")
                print("7. Keluar")
                choice = input("Pilih opsi (1/2/3/4/5/6/7): ")

                if choice == "1":
                    print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                    await fetch_latest_messages(app, 777000)
                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif choice == "3":
                    message_id = int(input("Masukkan ID pesan yang ingin dihapus: "))
                    await delete_message(app, 777000, message_id)
                elif choice == "4":
                    print("Melakukan pembaruan repo...")
                    os.system("git pull")
                    print("Repo telah diperbarui. Memulai ulang program...")
                    await asyncio.sleep(1)  # Menunggu sejenak sebelum memulai ulang
                    os.execv(sys.executable, ['python'] + sys.argv)  # Restart program
                elif choice == "5":
                    print(f"User ID: {me.id}")
                    print(f"Username: @{me.username}")
                    print(f"Nama: {me.first_name} {me.last_name if me.last_name else ''}")
                    print(f"Nomor Ponsel: {phone_number}")
                elif choice == "6":
                    api_id = input("Masukkan API ID: ")
                    api_hash = input("Masukkan API Hash: ")
                    await display_active_sessions(api_id, api_hash, session_string)
                elif choice == "7":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

            remove_pid_file()
    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor. Silakan login secara manual untuk mendapatkan string sesi yang baru.")

async def display_active_sessions(api_id, api_hash, session_string):
    async with PyrogramClient("active_sessions", api_id=api_id, api_hash=api_hash) as active_client:
        me = await active_client.get_me()
        print(f"Sesi Aktif untuk @{me.username}:")
        async for session in active_client.get_active_sessions():
            print(f"- ID: {session.id}, Device: {session.device}, Location: {session.location}")

async def main():
    check_if_running()

    print("Pilih metode login:")
    print("1. Login Baru")
    print("2. Login ke Akun Tersimpan")
    choice = input("Pilih opsi (1/2): ")

    if choice == "1":
        session_string = input("Masukkan string sesi Telegram (Pyrogram) Anda: ")
        await pyrogram_main(session_string)
    elif choice == "2":
        # Implementasi login ke akun tersimpan
        # Ini bisa diisi dengan logika untuk mengambil dan menggunakan session string yang tersimpan
        pass
    else:
        print("Pilihan tidak valid. Silakan pilih lagi.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
