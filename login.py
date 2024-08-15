from pyrogram import Client

# Masukkan string sesi Telegram kamu di sini
session_string = "masukkan_string_sesi_kamu_di_sini"

# Buat objek Client dengan menggunakan string sesi
app = Client("my_account", session_string=session_string)

# Jalankan Client
with app:
    # Dapatkan informasi akun yang sedang login
    me = app.get_me()
    print(me)
