import os
import asyncio
import json
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.auth import LogOutRequest
from telethon.tl.functions.messages import GetHistoryRequest, DeleteMessagesRequest

# File PID untuk memastikan hanya satu instance program yang berjalan
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

async def join_group_and_send_message(client, group_url, message_text):
    try:
        entity = await client.get_entity(group_url)
        await client(JoinChannelRequest(entity))
        await client.send_message(entity, message_text)
        print(f"Berhasil bergabung ke grup dan mengirim pesan: '{message_text}'")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

async def fetch_latest_messages(client, user_id, limit=5):
    try:
        messages = await client(GetHistoryRequest(
            peer=user_id,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        return messages.messages
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return []

async def delete_selected_messages(client, user_id, message_ids):
    try:
        await client(DeleteMessagesRequest(
            id=message_ids,
            revoke=True
        ))
        for message_id in message_ids:
            print(f"Pesan dengan ID {message_id} telah dihapus.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menghapus pesan: {e}")

async def kill_session(client):
    try:
        await client(LogOutRequest())
        print("Semua sesi telah dihentikan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menghentikan sesi: {e}")

async def telethon_main(session_string):
    client = TelegramClient(StringSession(session_string), api_id=123456, api_hash="your_api_hash")

    try:
        await client.start()
        me = await client.get_me()

        save_account(me.username or str(me.id), session_string)
        print(f"ID: {me.id}")
        print(f"Username: @{me.username}")
        print(f"Nama: {me.first_name} {me.last_name or ''}")

        while True:
            print("\nMenu:")
            print("1. Lihat 20 Pesan Terbaru dari 777000")
            print("2. Tunggu Pesan Masuk dari 777000")
            print("3. Hapus Pesan Terpilih dari 777000")
            print("4. Update Repo")
            print("5. Beralih Akun")
            print("6. Kill Session")
            print("7. Keluar")
            choice = input("Pilih opsi (1/2/3/4/5/6/7): ")

            if choice == "1":
                print("Menampilkan 20 pesan terbaru dari user ID 777000...")
                messages = await fetch_latest_messages(client, 777000, limit=20)
                for msg in messages:
                    print(f"Pesan ID {msg.id} dari {msg.chat_id}: {msg.message}")

            elif choice == "2":
                print("Menunggu pesan masuk dari user ID 777000...")
                @client.on(events.NewMessage(chats=777000))
                async def handle_incoming_message(event):
                    print(f"Pesan baru: {event.message.message}")
                await client.run_until_disconnected()

            elif choice == "3":
                print("Menghapus pesan terpilih dari user ID 777000...")
                messages = await fetch_latest_messages(client, 777000, limit=5)
                message_ids_to_delete = []

                for msg in messages:
                    print(f"Pesan ID {msg.id} dari {msg.chat_id}: {msg.message}")

                while True:
                    try:
                        delete_choice = input("Pilih ID pesan untuk dihapus (pisahkan dengan koma untuk beberapa pesan, atau ketik 'done' untuk selesai): ")
                        if delete_choice.lower() == 'done':
                            break
                        selected_ids = [int(num) for num in delete_choice.split(",")]
                        message_ids_to_delete = selected_ids
                        await delete_selected_messages(client, 777000, message_ids_to_delete)
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
                await kill_session(client)

            elif choice == "7":
                break
            else:
                print("Pilihan tidak valid. Silakan pilih lagi.")

        remove_pid_file()
    except SessionPasswordNeededError:
        print("Akun memerlukan autentikasi dua faktor. Silakan login secara manual.")
    finally:
        await client.disconnect()

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
        await telethon_main(session_string)
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
            session_string = input("Masukkan string sesi Telethon Anda: ")
            await telethon_main(session_string)
            break
        elif choice == "2":
            await switch_account()
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

try:
    asyncio.run(main())
finally:
    remove_pid_file()
