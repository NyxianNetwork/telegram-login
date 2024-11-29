
import os
import asyncio
import json
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

def save_account(account_name, session_string):
    accounts = load_accounts()
    accounts[account_name] = session_string
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)

def load_accounts():
    if os.path.isfile("accounts.json"):
        with open("accounts.json", "r") as f:
            return json.load(f)
    return {}

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
    return messages

async def delete_selected_messages(client, user_id, message_ids):
    await client.delete_messages(user_id, message_ids)
    for message_id in message_ids:
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
            save_account(me.username or str(me.id), session_string)

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
                print("6. Keluar")
                choice = input("Pilih opsi (1/2/3/4/5/6): ")

                if choice == "1":
                    print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                    messages = await fetch_latest_messages(app, 777000, limit=5)
                    for message in messages:
                        print(f"Pesan ID {message.id} dari {message.chat.id}: {message.text}")

                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    await asyncio.Future()  # Menunggu pesan secara asinkron

                elif choice == "3":
                    print("Menghapus pesan terpilih dari user ID 777000...")
                    messages = await fetch_latest_messages(app, 777000, limit=5)  # Ambil pesan terbaru lagi
                    message_ids_to_delete = []
                    
                    # Menampilkan pesan dengan ID dan meminta input dari pengguna
                    for message in messages:
                        print(f"Pesan ID {message.id} dari {message.chat.id}: {message.text}")
                    
                    # Meminta pengguna memilih pesan untuk dihapus
                    while True:
                        try:
                            delete_choice = input("Pilih ID pesan untuk dihapus (pisahkan dengan koma untuk beberapa pesan, atau ketik 'done' untuk selesai): ")
                            if delete_choice.lower() == 'done':
                                break
                            # Membagi pilihan berdasarkan koma dan mengubah ke integer
                            selected_ids = [int(num) for num in delete_choice.split(",")]
                            # Mengambil message_id berdasarkan pilihan
                            message_ids_to_delete = selected_ids
                            await delete_selected_messages(app, 777000, message_ids_to_delete)
                        except (ValueError, IndexError):
                            print("Pilihan tidak valid, silakan coba lagi.")
                
                elif choice == "4":
                    print("Melakukan update repo...")
                    os.system("git pull")  # Menjalankan git pull
                    print("Repo berhasil diperbarui.")

                elif choice == "5":
                    print("Beralih akun...")
                    await switch_account()  # Menjalankan fungsi untuk beralih akun

                elif choice == "6":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

            remove_pid_file()
    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor. Silakan login secara manual untuk mendapatkan string sesi yang baru.")

async def switch_account():
    accounts = load_accounts()
    if not accounts:
        print("Tidak ada akun yang disimpan.")
        return
    
    print("Akun yang tersedia:")
    for idx, account in enumerate(accounts.keys(), start=1):
        print(f"{idx}. {account}")

    choice = input("Pilih akun untuk beralih (masukkan nomor): ")
    try:
        choice = int(choice) - 1
        account_name = list(accounts.keys())[choice]
        session_string = accounts[account_name]
        await pyrogram_main(session_string)
    except (ValueError, IndexError):
        print("Pilihan tidak valid.")

async def main():
    check_if_running()

    print("Selamat datang di aplikasi Telegram CLI!")
    print("1. Login Baru")
    print("2. Login ke Akun Tersimpan")
    
    while True:
        choice = input("Pilih opsi (1/2): ")
        if choice == "1":
            session_string = input("Masukkan string sesi Telegram (Pyrogram) Anda: ")
            await pyrogram_main(session_string)
            break
        elif choice == "2":
            await switch_account()  # Memanggil fungsi untuk beralih akun
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
