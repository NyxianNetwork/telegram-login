import os
import asyncio
import json
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, BadRequestError

# File untuk menyimpan akun
accounts_file = "accounts.json"

# Fungsi untuk menyimpan akun
def save_account(account_name, session_string, api_id, api_hash):
    accounts = load_accounts()
    accounts[account_name] = {"session_string": session_string, "api_id": api_id, "api_hash": api_hash}
    with open(accounts_file, "w") as f:
        json.dump(accounts, f)

# Fungsi untuk memuat akun yang tersimpan
def load_accounts():
    if os.path.isfile(accounts_file):
        with open(accounts_file, "r") as f:
            return json.load(f)
    return {}

# Fungsi utama untuk menjalankan Telethon
async def telethon_main(api_id, api_hash, session_string):
    print("\nMencoba login menggunakan StringSession...")
    client = TelegramClient(StringSession(session_string), api_id, api_hash)

    try:
        async with client:
            me = await client.get_me()
            print(f"Berhasil login sebagai: {me.first_name} {me.last_name or ''} (@{me.username})")
            print(f"ID: {me.id}")

            # Menyimpan data akun
            save_account(me.username or str(me.id), session_string, api_id, api_hash)

            # Contoh: Menampilkan dialog yang tersedia
            print("\nDaftar chat yang tersedia:")
            async for dialog in client.iter_dialogs():
                print(f"- {dialog.name} ({dialog.id})")
    except SessionPasswordNeededError:
        print("Sesi tidak valid atau memerlukan autentikasi dua faktor. Harap login ulang.")
    except BadRequestError as e:
        print(f"Kesalahan saat mencoba login: {e}")
    except Exception as e:
        print(f"Kesalahan tidak terduga: {e}")

# Fungsi untuk login baru atau akun tersimpan
async def main():
    print("Selamat datang di aplikasi Telegram CLI!")
    print("1. Login Baru")
    print("2. Login ke Akun Tersimpan")

    choice = input("Pilih opsi (1/2): ")

    if choice == "1":
        # Meminta data API ID, API Hash, dan StringSession dari pengguna
        api_id = int(input("Masukkan API ID Anda: "))
        api_hash = input("Masukkan API Hash Anda: ")
        session_string = input("Masukkan string sesi Telethon Anda: ")
        await telethon_main(api_id, api_hash, session_string)

    elif choice == "2":
        accounts = load_accounts()
        if not accounts:
            print("Tidak ada akun yang disimpan. Silakan login baru terlebih dahulu.")
            return

        # Menampilkan daftar akun tersimpan
        print("Akun yang tersedia:")
        for idx, account_name in enumerate(accounts.keys(), start=1):
            print(f"{idx}. {account_name}")

        # Memilih akun dari daftar tersimpan
        account_choice = int(input("Pilih akun (masukkan nomor): "))
        account_name = list(accounts.keys())[account_choice - 1]
        account_data = accounts[account_name]

        # Login menggunakan data akun tersimpan
        api_id = account_data["api_id"]
        api_hash = account_data["api_hash"]
        session_string = account_data["session_string"]

        await telethon_main(api_id, api_hash, session_string)

    else:
        print("Pilihan tidak valid. Keluar.")

if __name__ == "__main__":
    asyncio.run(main())
