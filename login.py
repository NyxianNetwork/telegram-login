import os
import asyncio
import json
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
from telethon.sync import TelegramClient as TelethonClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.account import GetAuthorizations as TLGetAuthorizations, ResetAuthorization as TLResetAuthorization

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

async def pyrogram_kill_session(client):
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

async def telethon_kill_session(client):
    sessions = client(GetAuthorizations())
    print("\nDaftar sesi aktif:")
    for idx, session in enumerate(sessions.authorizations, 1):
        print(f"{idx}. Perangkat: {session.device_model} | IP: {session.ip} | Negara: {session.country} | Hash: {session.hash}")

    try:
        choice = int(input("\nPilih sesi yang ingin dihentikan (masukkan nomor): ")) - 1
        session_to_kill = sessions.authorizations[choice]
        client(TLResetAuthorization(hash=session_to_kill.hash))
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
            print_account_info(me)
            await display_menu(app, "pyrogram")
    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor.")

async def telethon_main(session_name):
    api_id = int(input("Masukkan API ID: "))
    api_hash = input("Masukkan API Hash: ")
    client = TelethonClient(session_name, api_id, api_hash)

    try:
        client.start()
        if client.is_user_authorized():
            me = client.get_me()
            print_account_info(me)
            await display_menu(client, "telethon")
    except SessionPasswordNeededError:
        print("Akun Anda memerlukan autentikasi dua faktor.")

def print_account_info(me):
    print(f"ID: {me.id}")
    print(f"Nama: {me.first_name} {me.last_name or ''}")
    print(f"Username: @{me.username}")
    print(f"Nomor Telepon: {me.phone}")

async def display_menu(client, client_type):
    while True:
        print("\nMenu:")
        print("1. Melihat 5 Pesan Terbaru")
        print("2. Killer Session")
        print("3. Keluar")

        choice = input("Pilih opsi (1/2/3): ")
        if choice == "1":
            await fetch_messages(client, client_type)
        elif choice == "2":
            if client_type == "pyrogram":
                await pyrogram_kill_session(client)
            else:
                await telethon_kill_session(client)
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid.")

async def fetch_messages(client, client_type):
    user_id = int(input("Masukkan user ID: "))
    limit = 5

    if client_type == "pyrogram":
        messages = [message async for message in client.get_chat_history(user_id, limit=limit)]
    else:
        messages = client.get_messages(user_id, limit=limit)

    for msg in messages:
        print(f"Pesan: {msg.text}")

async def main():
    check_if_running()

    print("Selamat datang di aplikasi Telegram CLI!")
    print("1. Login Baru dengan Pyrogram")
    print("2. Login Baru dengan Telethon")
    
    choice = input("Pilih opsi (1/2): ")
    if choice == "1":
        session_string = input("Masukkan string sesi: ")
        await pyrogram_main(session_string)
    elif choice == "2":
        session_name = input("Masukkan nama sesi: ")
        await telethon_main(session_name)
    else:
        print("Pilihan tidak valid.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
