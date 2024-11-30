import os
import asyncio
import json
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded
from telethon import TelegramClient as TelethonClient

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
            save_account(me.username or str(me.id), session_string)

            print(f"ID: {me.id}")
            print(f"Username: @{me.username}")
            print(f"Nama: {me.first_name} {me.last_name if me.last_name else ''}")

            while True:
                print("\nMenu:")
                print("1. Killer Session")
                print("2. Keluar")
                choice = input("Pilih opsi (1/2): ")

                if choice == "1":
                    await kill_session(app)

                elif choice == "2":
                    break

            remove_pid_file()
    except SessionPasswordNeeded:
        print("Akun Anda memerlukan autentikasi dua faktor.")

async def telethon_main(session_string):
    api_id = 123456  # Ganti dengan API ID Anda
    api_hash = "your_api_hash"  # Ganti dengan API Hash Anda
    client = TelethonClient("my_account", api_id, api_hash, session=session_string)

    try:
        async with client:
            me = await client.get_me()
            save_account(me.username or str(me.id), session_string)

            print(f"ID: {me.id}")
            print(f"Username: @{me.username}")
            print(f"Nama: {me.first_name} {me.last_name if me.last_name else ''}")

            while True:
                print("\nMenu:")
                print("1. Killer Session")
                print("2. Keluar")
                choice = input("Pilih opsi (1/2): ")

                if choice == "1":
                    print("Fungsi Killer Session belum diimplementasikan untuk Telethon.")
                elif choice == "2":
                    break

            remove_pid_file()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

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
            print("\nPilih metode login:")
            print("1. Login melalui Pyrogram string")
            print("2. Login melalui Telethon string")
            method_choice = input("Pilih metode (1/2): ")

            if method_choice == "1":
                session_string = input("Masukkan string sesi Pyrogram Anda: ")
                await pyrogram_main(session_string)
            elif method_choice == "2":
                session_string = input("Masukkan string sesi Telethon Anda: ")
                await telethon_main(session_string)
            else:
                print("Pilihan tidak valid.")
        elif choice == "2":
            await switch_account()
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
