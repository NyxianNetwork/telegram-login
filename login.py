import os
import json
import asyncio
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded, FloodWait, RPCError

# Fungsi untuk memeriksa apakah program sudah berjalan
pid_file = "program.pid"
accounts_file = "accounts.json"

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

def load_accounts():
    if os.path.isfile(accounts_file):
        with open(accounts_file, "r") as f:
            return json.load(f)
    return {}

def save_account(account_name, session_string):
    accounts = load_accounts()
    accounts[account_name] = session_string
    with open(accounts_file, "w") as f:
        json.dump(accounts, f)

async def fetch_latest_messages(client, user_id, limit=5):
    messages = []
    # Ambil pesan terbaru dari chat dengan user_id
    async for message in client.get_chat_history(user_id, limit=limit):
        messages.append(message)
    return messages

async def delete_message(client, user_id, message_id):
    try:
        await client.delete_messages(user_id, message_id)
        print(f"Pesan dengan ID {message_id} telah dihapus.")
    except FloodWait as e:
        print(f"Terjadi FloodWait. Tunggu {e.x} detik sebelum mencoba lagi.")
        await asyncio.sleep(e.x)  # Tunggu sesuai waktu FloodWait
        await delete_message(client, user_id, message_id)  # Coba lagi setelah menunggu
    except RPCError as e:
        print(f"Kesalahan saat menghapus pesan: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

async def pyrogram_main(session_string):
    app = PyrogramClient("my_account", session_string=session_string)

    @app.on_message(pyrogram_filters.chat(777000))
    async def handle_incoming_message(client, message):
        print(f"Pesan baru dari {message.chat.id}: {message.text}")

    try:
        async with app:
            me = await app.get_me()
            phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

            # Simpan akun yang berhasil login
            save_account(me.username or str(me.id), session_string)

            print(f"ID: {me.id}")
            print(f"Nomor: {phone_number}")
            print(f"Username: @{me.username}")
            print(f"Nama Lengkap: {me.first_name} {me.last_name if me.last_name else ''}")

            while True:
                print("\nMenu:")
                print("1. Melihat 5 Pesan Terbaru Dari user id 777000")
                print("2. Menunggu Pesan Masuk Dari user id 777000")
                print("3. Hapus 1 Pesan dari user id 777000")
                print("4. Update Repo")
                print("5. Beralih Akun")
                print("6. Keluar")
                choice = input("Pilih opsi (1/2/3/4/5/6): ")

                if choice == "1":
                    print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                    messages = await fetch_latest_messages(app, 777000, limit=5)
                    for idx, message in enumerate(messages, start=1):
                        print(f"{idx}. Pesan dari {message.chat.id}: {message.text}")
                    
                    print("\nHapus Pesan")
                    delete_choice = input("Masukkan nomor pesan yang ingin dihapus (atau tekan Enter untuk kembali): ")
                    if delete_choice.strip():
                        try:
                            delete_index = int(delete_choice) - 1
                            if 0 <= delete_index < len(messages):
                                await delete_message(app, messages[delete_index].chat.id, messages[delete_index].message_id)
                            else:
                                print("Nomor pesan tidak valid.")
                        except ValueError:
                            print("Input tidak valid, silakan masukkan nomor yang benar.")

                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    await asyncio.Future()  # Menunggu pesan secara asinkron
                elif choice == "3":
                    print("Menghapus pesan berdasarkan nomor urut dari user ID 777000...")
                    messages = await fetch_latest_messages(app, 777000, limit=5)
                    if messages:
                        for idx, message in enumerate(messages, start=1):
                            print(f"{idx}. Pesan dari {message.chat.id}: {message.text}")

                        delete_choice = input("Pilih nomor pesan untuk dihapus: ")
                        try:
                            delete_index = int(delete_choice) - 1
                            if 0 <= delete_index < len(messages):
                                await delete_message(app, messages[delete_index].chat.id, messages[delete_index].message_id)
                            else:
                                print("Nomor pesan tidak valid.")
                        except ValueError:
                            print("Input tidak valid, silakan masukkan nomor yang benar.")
                    else:
                        print("Tidak ada pesan untuk ditampilkan.")
                elif choice == "4":
                    print("Melakukan update repo...")
                    os.system("git pull")  # Menjalankan git pull
                    print("Repo berhasil diperbarui.")
                elif choice == "5":
                    print("Beralih akun...")
                    return  # Keluar dari fungsi ini untuk kembali ke main()
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
        print("Tidak ada akun yang tersimpan.")
        return

    print("Pilih akun untuk beralih:")
    for idx, account in enumerate(accounts.keys(), start=1):
        print(f"{idx}. {account}")

    choice = input("Pilih nomor akun: ")
    try:
        account_name = list(accounts.keys())[int(choice) - 1]
        session_string = accounts[account_name]
        print(f"Beralih ke akun: {account_name}")
        await pyrogram_main(session_string)
    except (ValueError, IndexError):
        print("Pilihan tidak valid.")

async def main():
    check_if_running()

    while True:
        print("\n1. Login Akun Baru")
        print("2. Beralih Akun")
        print("3. Keluar")
        choice = input("Pilih opsi (1/2/3): ")

        if choice == "1":
            session_string = input("Masukkan string sesi Telegram (Pyrogram) Anda: ")
            await pyrogram_main(session_string)
        elif choice == "2":
            await switch_account()
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
