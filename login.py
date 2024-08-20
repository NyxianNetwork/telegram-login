from pyrogram import Client

# Masukkan string sesi Telegram kamu di sini
session_string = "masukkan_string_sesi_kamu_di_sini"

# Buat objek Client dengan menggunakan string sesi
app = Client("my_account", session_string=session_string)

# Jalankan Client
with app:
    # Dapatkan informasi akun yang sedang login
    me = app.get_me()

    # Coba dapatkan nomor telepon (jika tersedia)
    phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

    print(f"Nama: {me.first_name} {me.last_name if me.last_name else ''}")
    print(f"Username: @{me.username}")
    print(f"Nomor Telepon: {phone_number}")
