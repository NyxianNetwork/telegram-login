import os
import asyncio
import json
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization

pid_file = "program.pid"
ACCOUNT_FILE = "accounts.json"

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

def load_accounts():
    if os.path.isfile(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Terjadi kesalahan dalam membaca accounts.json.")
                return {}
    return {}

def save_account(username, session_string):
    accounts = load_accounts()
    accounts[username] = session_string
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

async def fetch_latest_messages(client, user_id, limit=5):
    messages = []
    async for message in client.get_chat_history(user_id, limit=limit):
        messages.append(message)
    return messages

async def delete_selected_messages(client, user_id, message_ids):
    await client.delete_messages(user_id, message_ids)
    for message_id in message_ids:
        print(f"Pesan dengan ID {message_id} telah dihapus.")

async def kill_session(client):
    sessions = (await client.invoke(GetAuthorizations())).authorizations
    print("\nDaftar sesi aktif:")
    for idx, session in enumerate(sessions, 1):
        print(f"{idx}. Perangkat: {session.device_model} | IP: {session.ip} | Negara: {session.country} | Hash: {session.hash}")

    try:
        choice = int(input("\nPilih sesi yang ingin dihentikan (masukkan nomor): ")) - 1
        session_to_kill = sessions[choice]
        await client.invoke(ResetAuthorization(hash=session_to_kill.hash))
        print("Sesi berhasil dihentikan.")
    except (IndexError, ValueError):
        print("Pilihan tidak valid.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menghentikan sesi: {e}")

async def pyrogram_main(session_string):
    app = PyrogramClient("my_account", session_string=session_string)

    try:
        async with app:
            me = await app.get_me()
            phone_number = me.phone_number if me.phone_number else "Tidak tersedia"
            username = me.username if me.username else "Tidak ada username"
            full_name = f"{me.first_name} {me.last_name if me.last_name else ''}".strip()

            print("\n===== BERHASIL LOGIN =====")
            print(f"ID: {me.id}")
            print(f"Nomor Telepon: {phone_number}")
            print(f"Username: @{username}")
            print(f"Nama: {full_name}")
            print("==========================\n")

            save_account(username, session_string)

            while True:
                print("\nMenu:")
                print("1. Lihat 5 Pesan Terbaru dari 777000")
                print("2. Tunggu Pesan Masuk dari 777000")
                print("3. Hapus Pesan Terpilih dari 777000")
                print("4. Update Repo")
                print("5. Beralih Akun")
                print("6. Keluar Sesi Aktif")
                print("7. Keluar Program")
                print("8. Ganti Nama Menjadi 'HACK BY NOCTYRA'")
                print("9. Ganti Username Akun")

                choice = input("Pilih opsi (1/2/3/4/5/6/7/8/9): ").strip()

                if choice == "1":
                    print("Menampilkan 5 pesan terbaru dari user ID 777000...")
                    messages = await fetch_latest_messages(app, 777000, limit=5)
                    for message in messages:
                        print(f"Pesan ID {message.id}: {message.text}")

                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    @app.on_message(pyrogram_filters.chat(777000))
                    async def handle_incoming_message(client, message):
                        print(f"Pesan baru dari {message.chat.id}: {message.text}")
                    await asyncio.Future()

                elif choice == "3":
                    print("Menghapus pesan terpilih dari user ID 777000...")
                    messages = await fetch_latest_messages(app, 777000, limit=5)
                    message_ids_to_delete = []
                    for message in messages:
                        print(f"Pesan ID {message.id}: {message.text}")
                    while True:
                        try:
                            delete_choice = input("Pilih ID pesan untuk dihapus (pisahkan dengan koma, atau ketik 'done'): ")
                            if delete_choice.lower() == 'done':
                                break
                            selected_ids = [int(num) for num in delete_choice.split(",")]
                            message_ids_to_delete = selected_ids
                            await delete_selected_messages(app, 777000, message_ids_to_delete)
                        except (ValueError, IndexError):
                            print("Pilihan tidak valid, silakan coba lagi.")

                elif choice == "4":
                    print("Melakukan update repo...")
                    os.system("git pull")
                    print("Repo berhasil diperbarui.")

                elif choice == "5":
                    print("Beralih akun...")
                    await switch_account()

                elif choice == "6":
                    await kill_session(app)

                elif choice == "7":
                    break

                elif choice == "8":
                    print("Mengubah nama akun...")
                    try:
                        await app.update_profile(first_name="HACK BY NOCTYRA", last_name="")
                        print("✅ Nama berhasil diubah menjadi 'HACK BY NOCTYRA'")
                    except Exception as e:
                        print(f"❌ Gagal mengubah nama: {e}")

                elif choice == "9":
                    new_username = input("Masukkan username baru yang diinginkan (tanpa '@'): ").strip()
                    try:
                        await app.update_username(new_username)
                        print(f"✅ Username berhasil diubah menjadi @{new_username}")
                    except Exception as e:
                        print(f"❌ Gagal mengubah username: {e}")

                else:
                    print("Pilihan tidak valid. Silakan pilih lagi.")

            remove_pid_file()

    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor. Silakan login secara manual untuk mendapatkan string sesi yang baru.")

async def switch_account():
    accounts = load_accounts()
    if not isinstance(accounts, dict) or not accounts:
        print("Tidak ada akun yang tersimpan atau format file accounts.json rusak.")
        return

    valid_accounts = {}

    print("\nMemeriksa status akun tersimpan...")
    for username, session_string in accounts.items():
        print(f"Mengecek akun {username}...")
        temp_client = PyrogramClient("temp_session", session_string=session_string)
        try:
            async with temp_client:
                me = await temp_client.get_me()
                if me:
                    valid_accounts[username] = session_string
                    print(f"✅ Akun {username} masih aktif.")
        except Exception:
            print(f"❌ Akun {username} tidak valid atau telah dihapus.")

    if len(valid_accounts) != len(accounts):
        print("\nMenghapus akun yang tidak valid dari daftar...")
        with open(ACCOUNT_FILE, "w") as f:
            json.dump(valid_accounts, f, indent=4)

    if not valid_accounts:
        print("Tidak ada akun yang tersedia setelah verifikasi.")
        return

    print("\nAkun yang tersedia:")
    for idx, username in enumerate(valid_accounts.keys(), start=1):
        print(f"{idx}. {username}")

    choice = input("Pilih akun untuk beralih (masukkan nomor, atau ketik 'batal'): ")
    if choice.lower() == "batal":
        return

    try:
        session_string = list(valid_accounts.values())[int(choice) - 1]
        print("\nBeralih ke akun...")
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
            await switch_account()
            break
        else:
            print("Pilihan tidak valid.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()

