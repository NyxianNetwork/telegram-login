import os
import asyncio
import json
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest, DeleteMessagesRequest
from telethon.tl.functions.auth import LogOutRequest

# File untuk menyimpan akun
accounts_file = "accounts.json"

def save_account(account_name, session_string, api_id, api_hash):
    accounts = load_accounts()
    accounts[account_name] = {"session_string": session_string, "api_id": api_id, "api_hash": api_hash}
    with open(accounts_file, "w") as f:
        json.dump(accounts, f)

def load_accounts():
    if os.path.isfile(accounts_file):
        with open(accounts_file, "r") as f:
            return json.load(f)
    return {}

async def fetch_latest_messages(client, chat_id, limit=5):
    try:
        history = await client(GetHistoryRequest(
            peer=chat_id,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        return history.messages
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil pesan: {e}")
        return []

async def delete_selected_messages(client, chat_id, message_ids):
    try:
        await client(DeleteMessagesRequest(id=message_ids, revoke=True))
        print(f"Pesan dengan ID {message_ids} berhasil dihapus.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menghapus pesan: {e}")

async def kill_session(client):
    try:
        await client(LogOutRequest())
        print("Sesi telah dihentikan.")
    except Exception as e:
        print(f"Kesalahan saat menghentikan sesi: {e}")

async def telethon_main(api_id, api_hash, session_string):
    client = TelegramClient(StringSession(session_string), api_id, api_hash)

    try:
        await client.start()
        me = await client.get_me()

        # Menyimpan data akun
        save_account(me.username or str(me.id), session_string, api_id, api_hash)

        print(f"Berhasil login sebagai: {me.first_name} {me.last_name or ''} (@{me.username})")
        print(f"ID: {me.id}")

        while True:
            print("\nMenu:")
            print("1. Lihat 20 Pesan Terbaru dari 777000")
            print("2. Hapus Pesan Terpilih dari 777000")
            print("3. Logout")
            print("4. Keluar")
            choice = input("Pilih opsi (1/2/3/4): ")

            if choice == "1":
                messages = await fetch_latest_messages(client, 777000, limit=20)
                for msg in messages:
                    print(f"Pesan ID {msg.id}: {msg.message}")

            elif choice == "2":
                messages = await fetch_latest_messages(client, 777000, limit=5)
                print("Pesan terbaru:")
                for msg in messages:
                    print(f"Pesan ID {msg.id}: {msg.message}")

                ids_to_delete = input("Masukkan ID pesan yang ingin dihapus (pisahkan dengan koma): ").split(",")
                ids_to_delete = [int(x.strip()) for x in ids_to_delete if x.strip().isdigit()]
                await delete_selected_messages(client, 777000, ids_to_delete)

            elif choice == "3":
                await kill_session(client)
                break

            elif choice == "4":
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    except SessionPasswordNeededError:
        print("Akun memerlukan autentikasi dua faktor. Silakan login secara manual.")
    except Exception as e:
        print(f"Kesalahan: {e}")
    finally:
        await client.disconnect()

async def main():
    print("Selamat datang di aplikasi Telegram CLI!")
    print("1. Login Baru")
    print("2. Login ke Akun Tersimpan")

    choice = input("Pilih opsi (1/2): ")

    if choice == "1":
        api_id = int(input("Masukkan API ID Anda: "))
        api_hash = input("Masukkan API Hash Anda: ")
        session_string = input("Masukkan string sesi Telethon Anda: ")
        await telethon_main(api_id, api_hash, session_string)

    elif choice == "2":
        accounts = load_accounts()
        if not accounts:
            print("Tidak ada akun yang disimpan. Silakan login baru terlebih dahulu.")
            return

        print("Akun yang tersedia:")
        for idx, account_name in enumerate(accounts.keys(), start=1):
            print(f"{idx}. {account_name}")

        account_choice = int(input("Pilih akun (masukkan nomor): "))
        account_name = list(accounts.keys())[account_choice - 1]
        account_data = accounts[account_name]

        api_id = account_data["api_id"]
        api_hash = account_data["api_hash"]
        session_string = account_data["session_string"]

        await telethon_main(api_id, api_hash, session_string)

    else:
        print("Pilihan tidak valid. Keluar.")

if __name__ == "__main__":
    asyncio.run(main())
