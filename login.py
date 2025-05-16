import os
import asyncio
import json
from typing import Dict, List, Optional
from pyrogram import Client as PyrogramClient, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
from pyrogram.types import Message

pid_file = "program.pid"
ACCOUNT_FILE = "accounts.json"


def check_if_running() -> None:
    if os.path.isfile(pid_file):
        print("Program sudah berjalan sebelumnya!")
        exit()
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))


def remove_pid_file() -> None:
    if os.path.isfile(pid_file):
        os.remove(pid_file)


def load_accounts() -> Dict[str, str]:
    if not os.path.isfile(ACCOUNT_FILE):
        return {}
    try:
        with open(ACCOUNT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Terjadi kesalahan dalam membaca accounts.json.")
        return {}


def save_account(username: str, session_string: str) -> None:
    accounts = load_accounts()
    accounts[username] = session_string
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(accounts, f, indent=4)


async def fetch_latest_messages(client: PyrogramClient, user_id: int, limit: int = 5) -> List[Message]:
    return [msg async for msg in client.get_chat_history(user_id, limit=limit)]


async def delete_selected_messages(client: PyrogramClient, user_id: int, message_ids: List[int]) -> None:
    await client.delete_messages(user_id, message_ids)
    for msg_id in message_ids:
        print(f"Pesan dengan ID {msg_id} telah dihapus.")


async def kill_session(client: PyrogramClient) -> None:
    try:
        result = await client.invoke(GetAuthorizations())
        sessions = result.authorizations

        if not sessions:
            print("Tidak ada sesi aktif.")
            return

        print("\nDaftar sesi aktif:")
        for idx, session in enumerate(sessions, 1):
            print(f"{idx}. Perangkat: {session.device_model} | IP: {session.ip} | Negara: {session.country}")

        choice = int(input("Pilih sesi untuk dihentikan (nomor): ")) - 1
        if 0 <= choice < len(sessions):
            await client.invoke(ResetAuthorization(hash=sessions[choice].hash))
            print("Sesi berhasil dihentikan.")
        else:
            print("Pilihan tidak valid.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menghentikan sesi: {e}")


async def pyrogram_main(session_string: str) -> None:
    app = PyrogramClient("my_account", session_string=session_string)
    try:
        async with app:
            me = await app.get_me()
            phone_number = me.phone_number or "Tidak tersedia"
            username = me.username or f"id_{me.id}"
            full_name = f"{me.first_name} {me.last_name or ''}".strip()

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
                choice = input("Pilih opsi (1/2/3/4/5/6/7): ").strip()

                if choice == "1":
                    messages = await fetch_latest_messages(app, 777000)
                    for msg in messages:
                        print(f"ID {msg.id}: {msg.text or '[Media atau Kosong]'}")

                elif choice == "2":
                    print("Menunggu pesan masuk dari user ID 777000...")
                    @app.on_message(filters.chat(777000))
                    async def handle_incoming_message(_, msg: Message):
                        print(f"Pesan dari {msg.chat.id}: {msg.text or '[Media atau Kosong]'}")
                    await asyncio.Future()

                elif choice == "3":
                    messages = await fetch_latest_messages(app, 777000)
                    for msg in messages:
                        print(f"ID {msg.id}: {msg.text or '[Media atau Kosong]'}")
                    raw_input = input("Masukkan ID pesan yang akan dihapus (pisahkan dengan koma): ")
                    try:
                        ids = list(map(int, raw_input.strip().split(",")))
                        await delete_selected_messages(app, 777000, ids)
                    except Exception:
                        print("Input tidak valid.")

                elif choice == "4":
                    print("Menjalankan git pull...")
                    os.system("git pull")

                elif choice == "5":
                    await switch_account()

                elif choice == "6":
                    await kill_session(app)

                elif choice == "7":
                    break

                else:
                    print("Pilihan tidak valid.")

    except SessionPasswordNeeded:
        print("Akun ini memerlukan autentikasi dua faktor.")
    except Exception as e:
        print(f"Kesalahan saat login: {e}")
    finally:
        remove_pid_file()


async def switch_account() -> None:
    accounts = load_accounts()
    if not accounts:
        print("Tidak ada akun yang tersimpan.")
        return

    valid_accounts = {}

    print("\nMemeriksa akun yang tersedia...")
    for username, session_string in accounts.items():
        try:
            temp_client = PyrogramClient("temp_check", session_string=session_string)
            async with temp_client:
                me = await temp_client.get_me()
                if me:
                    valid_accounts[username] = session_string
                    print(f"✅ {username} aktif")
        except Exception:
            print(f"❌ {username} tidak bisa diakses")

    if not valid_accounts:
        print("Semua akun tidak valid.")
        with open(ACCOUNT_FILE, "w") as f:
            json.dump({}, f)
        return

    if len(valid_accounts) != len(accounts):
        print("Memperbarui daftar akun...")
        with open(ACCOUNT_FILE, "w") as f:
            json.dump(valid_accounts, f, indent=4)

    print("\nDaftar akun:")
    for idx, uname in enumerate(valid_accounts.keys(), 1):
        print(f"{idx}. {uname}")

    try:
        choice = input("Pilih akun (nomor) atau ketik 'batal': ")
        if choice.lower() == "batal":
            return
        selected = list(valid_accounts.values())[int(choice) - 1]
        await pyrogram_main(selected)
    except (IndexError, ValueError):
        print("Pilihan tidak valid.")


async def main() -> None:
    check_if_running()
    print("Selamat datang di Telegram CLI")
    print("1. Login Baru")
    print("2. Gunakan Akun Tersimpan")

    while True:
        opt = input("Pilih opsi (1/2): ").strip()
        if opt == "1":
            session = input("Masukkan string sesi Anda: ")
            await pyrogram_main(session)
            break
        elif opt == "2":
            await switch_account()
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        remove_pid_file()
