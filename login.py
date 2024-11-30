import os
import asyncio
import json
from pyrogram import Client as PyrogramClient
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
from telethon import TelegramClient
from telethon.sessions import StringSession

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

def save_account(account_name, session_string, client_type, api_id=None, api_hash=None):
    accounts = load_accounts()
    accounts[account_name] = {
        "session": session_string,
        "client_type": client_type,
        "api_id": api_id,
        "api_hash": api_hash
    }
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)

def load_accounts():
    if os.path.isfile("accounts.json"):
        with open("accounts.json", "r") as f:
            return json.load(f)
    return {}

async def fetch_latest_messages_pyrogram(client, user_id, limit=5):
    messages = []
    async for message in client.get_chat_history(user_id, limit=limit):
        messages.append(message)
    return messages

async def fetch_latest_messages_telethon(client, user_id, limit=5):
    return await client.get_messages(user_id, limit=limit)

async def kill_session_pyrogram(client):
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

    async with app:
        me = await app.get_me()
        save_account(me.username or str(me.id), session_string, "pyrogram")

        print(f"ID: {me.id}")
        print(f"Nomor: {me.phone_number if me.phone_number else 'Nomor telepon tidak tersedia'}")
        print(f"Username: @{me.username}")
        print(f"Nama Lengkap: {me.first_name} {me.last_name or ''}")

        await menu_loop(app, "pyrogram")

async def telethon_main(session_string, api_id, api_hash):
    app = TelegramClient(StringSession(session_string), api_id, api_hash)

    async with app:
        await app.connect()
        me = await app.get_me()
        save_account(me.username or str(me.id), session_string, "telethon", api_id, api_hash)

        print(f"ID: {me.id}")
        print(f"Nomor: {me.phone if me.phone else 'Nomor telepon tidak tersedia'}")
        print(f"Username: @{me.username}")
        print(f"Nama Lengkap: {me.first_name} {me.last_name or ''}")

        await menu_loop(app, "telethon")

async def menu_loop(client, client_type):
    while True:
        print("\nMenu:")
        print("1. Melihat 5 Pesan Terbaru dari user ID 777000")
        print("2. Beralih Akun")
        print("3. Killer Session")
        print("4. Keluar")
        choice = input("Pilih opsi (1/2/3/4): ")

        if choice == "1":
            if client_type == "pyrogram":
                messages = await fetch_latest_messages_pyrogram(client, 777000)
            else:
                messages = await fetch_latest_messages_telethon(client, 777000)
            for msg in messages:
                print(f"Pesan ID {msg.id}: {msg.text}")

        elif choice == "2":
            await switch_account()

        elif choice == "3":
            if client_type == "pyrogram":
                await kill_session_pyrogram(client)
            else:
                print("Killer session hanya tersedia di Pyrogram.")

        elif choice == "4":
            break

        else:
            print("Pilihan tidak valid.")

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
        session_info = accounts[account_name]
        if session_info["client_type"] == "pyrogram":
            await pyrogram_main(session_info["session"])
        else:
            await telethon_main(session_info["session"], session_info["api_id"], session_info["api_hash"])
    except (ValueError, IndexError):
        print("Pilihan tidak valid.")

async def main():
    check_if_running()

    print("Selamat datang di aplikasi Telegram CLI!")
    print("1. Login Baru (Pyrogram)")
    print("2. Login Baru (Telethon)")
    print("3. Login ke Akun Tersimpan")

    while True:
        choice = input("Pilih opsi (1/2/3): ")
        if choice == "1":
            session_string = input("Masukkan string sesi Telegram (Pyrogram) Anda: ")
            await pyrogram_main(session_string)
            break
        elif choice == "2":
            api_id = int(input("Masukkan API ID Anda: "))
            api_hash = input("Masukkan API Hash Anda: ")
            session_string = input("Masukkan string sesi Telegram (Telethon) Anda: ")
            await telethon_main(session_string, api_id, api_hash)
            break
        elif choice == "3":
            await switch_account()
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
