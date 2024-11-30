import os
import asyncio
import json
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

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

def save_account(account_name, session_string, client_type):
    accounts = load_accounts()
    accounts[account_name] = {"session_string": session_string, "client_type": client_type}
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)

def load_accounts():
    if os.path.isfile("accounts.json"):
        with open("accounts.json", "r") as f:
            return json.load(f)
    return {}

async def kill_session_telethon(client):
    try:
        print("Mengakhiri semua sesi kecuali sesi saat ini...")
        await client(functions.auth.LogOutRequest())
        print("Sesi lainnya telah diakhiri.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengakhiri sesi: {e}")

async def pyrogram_main(session_string):
    app = PyrogramClient("my_account", session_string=session_string)

    try:
        async with app:
            me = await app.get_me()
            save_account(me.username or str(me.id), session_string, "pyrogram")
            print(f"Login sebagai: {me.first_name} {me.last_name if me.last_name else ''} (@{me.username})")

            while True:
                print("\nMenu Pyrogram:")
                print("1. Killer Session")
                print("2. Keluar")
                choice = input("Pilih opsi (1/2): ")

                if choice == "1":
                    await kill_session_pyrogram(app)
                elif choice == "2":
                    break
                else:
                    print("Pilihan tidak valid.")
    except SessionPasswordNeeded:
        print("Autentikasi dua faktor diperlukan.")

async def telethon_main(api_id, api_hash, session_name):
    client = TelegramClient(session_name, api_id, api_hash)

    try:
        await client.start()
        me = await client.get_me()
        session_string = await client.export_session_string()
        save_account(me.username or str(me.id), session_string, "telethon")

        print(f"Login sebagai: {me.first_name} {me.last_name if me.last_name else ''} (@{me.username})")

        while True:
            print("\nMenu Telethon:")
            print("1. Killer Session")
            print("2. Keluar")
            choice = input("Pilih opsi (1/2): ")

            if choice == "1":
                await kill_session_telethon(client)
            elif choice == "2":
                break
            else:
                print("Pilihan tidak valid.")
    except SessionPasswordNeededError:
        print("Autentikasi dua faktor diperlukan.")

async def switch_account():
    accounts = load_accounts()
    if not accounts:
        print("Tidak ada akun yang disimpan.")
        return
    
    print("Akun yang tersedia:")
    for idx, account in enumerate(accounts.keys(), start=1):
        print(f"{idx}. {account} ({accounts[account]['client_type']})")

    choice = input("Pilih akun untuk beralih (masukkan nomor): ")
    try:
        choice = int(choice) - 1
        account_name = list(accounts.keys())[choice]
        account_data = accounts[account_name]
        session_string = account_data["session_string"]
        client_type = account_data["client_type"]

        if client_type == "pyrogram":
            await pyrogram_main(session_string)
        elif client_type == "telethon":
            api_id = input("Masukkan API ID: ")
            api_hash = input("Masukkan API Hash: ")
            await telethon_main(api_id, api_hash, account_name)
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
            session_string = input("Masukkan string sesi Pyrogram Anda: ")
            await pyrogram_main(session_string)
            break
        elif choice == "2":
            api_id = input("Masukkan API ID: ")
            api_hash = input("Masukkan API Hash: ")
            session_name = input("Masukkan nama sesi Telethon: ")
            await telethon_main(api_id, api_hash, session_name)
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
