import os
import asyncio
import json
from pyrogram import Client as PyrogramClient, filters as pyrogram_filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization

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

def save_account(account_data):
    """Menyimpan data akun ke dalam file JSON."""
    accounts = load_accounts()
    accounts[account_data["username"] or str(account_data["id"])] = account_data
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

async def pyrogram_main(session_string):
    """Mengelola sesi Pyrogram dan menampilkan informasi akun setelah login."""
    app = PyrogramClient("my_account", session_string=session_string)

    try:
        async with app:
            me = await app.get_me()

            # Ambil informasi akun
            account_info = {
                "id": me.id,
                "phone_number": me.phone_number if me.phone_number else "Tidak tersedia",
                "username": me.username if me.username else "Tidak ada username",
                "name": f"{me.first_name} {me.last_name if me.last_name else ''}".strip(),
                "session_string": session_string
            }

            # Simpan ke dalam file akun
            save_account(account_info)

            # Tampilkan informasi akun di terminal
            print("\n===== INFORMASI AKUN =====")
            print(f"ID: {account_info['id']}")
            print(f"Nomor Telepon: {account_info['phone_number']}")
            print(f"Username: @{account_info['username']}")
            print(f"Nama: {account_info['name']}")
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
    for idx, (username, data) in enumerate(accounts.items(), start=1):
        if isinstance(data, dict) and "session_string" in data:
            print(f"{idx}. {data.get('name', 'Tanpa Nama')} ({data.get('phone_number', 'Tidak tersedia')}) - @{data.get('username', 'Tidak ada username')}")
        else:
            print(f"{idx}. Format akun tidak valid, harap periksa accounts.json.")

    choice = input("Pilih akun untuk beralih (masukkan nomor, atau ketik 'batal' untuk kembali): ")
    if choice.lower() == "batal":
        return

    try:
        account_data = list(accounts.values())[int(choice) - 1]
        print(f"\n===== BERPINDAH KE AKUN =====")
        print(f"ID: {account_data['id']}")
        print(f"Nomor Telepon: {account_data['phone_number']}")
        print(f"Username: @{account_data['username']}")
        print(f"Nama: {account_data['name']}")
        print("=============================\n")
        
        await pyrogram_main(account_data["session_string"])
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
