import os
import asyncio
import json
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded

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
    """Memuat daftar akun dari file JSON."""
    if os.path.isfile(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Terjadi kesalahan dalam membaca accounts.json. Format tidak valid.")
                return {}
    return {}

async def pyrogram_main(session_string):
    """Mengelola sesi Pyrogram dan menampilkan informasi akun setelah login."""
    app = PyrogramClient("my_account", session_string=session_string)

    try:
        async with app:
            me = await app.get_me()

            # Ambil informasi akun
            phone_number = me.phone_number if me.phone_number else "Tidak tersedia"
            username = me.username if me.username else "Tidak ada username"
            full_name = f"{me.first_name} {me.last_name if me.last_name else ''}".strip()

            # Tampilkan informasi akun di terminal
            print("\n===== BERHASIL LOGIN =====")
            print(f"ID: {me.id}")
            print(f"Nomor Telepon: {phone_number}")
            print(f"Username: @{username}")
            print(f"Nama: {full_name}")
            print("==========================\n")

    except SessionPasswordNeeded:
        print("Akun membutuhkan autentikasi dua faktor. Silakan login manual untuk mendapatkan string sesi baru.")

async def switch_account():
    """Memungkinkan pengguna beralih ke akun lain."""
    accounts = load_accounts()
    
    if not isinstance(accounts, dict) or not accounts:
        print("Tidak ada akun yang tersimpan atau format file accounts.json rusak.")
        return

    print("\nAkun yang tersedia:")
    for idx, username in enumerate(accounts.keys(), start=1):
        print(f"{idx}. {username}")

    choice = input("Pilih akun untuk beralih (masukkan nomor, atau ketik 'batal' untuk kembali): ")
    if choice.lower() == "batal":
        return

    try:
        session_string = list(accounts.values())[int(choice) - 1]

        print("\nBeralih ke akun...")
        await pyrogram_main(session_string)
    except (ValueError, IndexError):
        print("Pilihan tidak valid.")

async def main():
    """Menjalankan menu utama login."""
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
