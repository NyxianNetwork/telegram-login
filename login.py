import os
import asyncio
from pyrogram import Client

# Masukkan string sesi Telegram kamu di sini
session_string = "BQE1hwoAOSNalnW8B5IXq3BbCMZoU3N64elZ-bR7qvrxF7X8dD1GVDGui05KHh9k3vnCplQ2FxeOFNfvsrnE9ZzuOg8mY3mFBmXezVT08N-ulyTe88TpYaqMlgk_GlhRkKOHXkv1oYnDkP88SJlUw-QXAYHOrNkbOuz6tfImsu1T2usjWa65NifnGDJEcsfNt7of4mdQH4j6natxbYZLJpg4lRuvQnkKa4H6vfrhlGckm_uz-eNeYjg01i12zJ9nWiSJHvtfC5YK45tmmWQDKmzla6lgpip1Ms7QsoVmwYu_jMAW1u5XEZN8KjmTmT3UJGw5yRTTJ04yWiMlgeNgAAAB3d6goAA"

# Buat objek Client dengan menggunakan string sesi
app = Client("my_account", session_string=session_string)

# ID User untuk memfilter pesan
user_id = 777000

# Cek apakah program sudah berjalan
pid_file = "program.pid"

def check_if_running():
    if os.path.isfile(pid_file):
        print("Program sudah berjalan sebelumnya!")
    else:
        # Simpan PID (Process ID) program ini ke dalam file
        with open(pid_file, "w") as f:
            f.write(str(os.getpid()))

def remove_pid_file():
    if os.path.isfile(pid_file):
        os.remove(pid_file)

async def fetch_latest_messages(client, user_id, limit=5):
    # Ambil pesan terbaru dari chat dengan user_id
    async for message in client.get_chat_history(user_id, limit=limit):
        print(f"Pesan dari {message.chat.id}: {message.text}")

async def main():
    check_if_running()

    async with app:
        # Dapatkan informasi akun yang sedang login
        me = await app.get_me()

        # Coba dapatkan nomor telepon (jika tersedia)
        phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

        print(f"Nama: {me.first_name} {me.last_name if me.last_name else ''}")
        print(f"Username: @{me.username}")
        print(f"Nomor Telepon: {phone_number}")

        print(f"Menampilkan 5 pesan terbaru dari user ID {user_id}...")

        # Fetch and display the latest messages
        await fetch_latest_messages(app, user_id)

        # Menghentikan program setelah menampilkan pesan
        remove_pid_file()

try:
    asyncio.run(main())
finally:
    remove_pid_file()
