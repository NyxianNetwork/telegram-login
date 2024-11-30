import os
import asyncio
import json
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
from telethon import TelegramClient as TelethonClient

# Konfigurasi API (API_ID dan API_HASH diatur di sini)
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"

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

async def fetch_latest_messages(client, user_id, limit=5):
    messages = []
    async for message in client.get_chat_history(user_id, limit=limit):
        messages.append(message)
    return messages

async def delete_selected_messages(client, user_id, message_ids):
    await client.delete_messages(user_id, message_ids)
    for message_id in message_ids:
        print(f"Pesan dengan ID {message_id} telah dihapus.")

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
    app = PyrogramClient("pyrogram_account", session_string=session_string)

    @app.on_message(pyrogram_filters.chat(777000))
    async def handle_incoming_message(client, message):
        print(f"Pesan baru dari {message.chat.id}: {message.text}")

    try:
        async with app:
            me = await app.get_me()
            print(f"ID: {me.id}\nNama: {me.first_name}")

            while True:
                print("\nMenu Pyrogram:")
                print("1. Lihat Pesan Terbaru")
                print("2. Hapus Pesan")
                print("3. Killer Session")
                print("4. Keluar")

                choice = input("Pilih opsi (1/2/3/4): ")

                if choice == "1":
                    messages = await fetch_latest_messages(app, 777000, limit=5)
                    for msg in messages:
                        print(f"ID: {msg.id} - {msg.text}")

                elif choice == "2":
                    message_ids = input("Masukkan ID pesan yang akan dihapus (pisahkan dengan koma): ")
                    await delete_selected_messages(app, 777000, [int(id) for id in message_ids.split(",")])

                elif choice == "3":
                    await kill_session_pyrogram(app)

                elif choice == "4":
                    break
    except SessionPasswordNeeded:
        print("Sesi membutuhkan autentikasi dua faktor!")

async def telethon_main():
    client = TelethonClient("telethon_account", API_ID, API_HASH)
    await client.start()

    me = await client.get_me()
    print(f"ID: {me.id}\nNama: {me.first_name}")

    while True:
        print("\nMenu Telethon:")
        print("1. Keluar")
        choice = input("Pilih opsi (1): ")

        if choice == "1":
            break

async def main():
    check_if_running()

    print("Pilih metode login:")
    print("1. Pyrogram")
    print("2. Telethon")

    method = input("Metode (1/2): ")
    if method == "1":
        session_string = input("Masukkan string sesi Pyrogram: ")
        await pyrogram_main(session_string)
    elif method == "2":
        await telethon_main()
    else:
        print("Pilihan tidak valid.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
