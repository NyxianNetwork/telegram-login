import os
import sys
from pyrogram import Client, filters

# Masukkan string sesi yang sudah kamu miliki
session_string = "AQFFwxoAwX35DhN5Wq7p9tp6JJsdaGYuYJXBPj-MaEKn5nqWLlkPZ84nfkSpSTo997P5l5k7j6NqeqthZXwzthUFCl9ucgrxXCzvPayoxA75a4JehVbrztoRn9rH7Opb92wFs3dacOiJAqlNiAZ0WjsVgPVlg8iCRQUOy5OSCnGf6BfJlBTXOmnwFxmpJur7JJglSEFYo01s1zfctVPZ-nM7AzsZzsYN_nw3_HoUc4TFmwfMxe8xuzJ6w0b6ahqnUERjgly7A3CjKy7lw7vz1LTeDXmAjbkkVkH5nkOC0dbivUmDKV53llm2DzmFV2Wm6YqkxJv_FKXbxRZE2lpDePayk_UuIgAAAABs_9IyAA"

# Buat objek Client dengan menggunakan string sesi
app = Client("my_account", session_string=session_string)

# Cek apakah program sudah berjalan
pid_file = "program.pid"

def check_if_running():
    if os.path.isfile(pid_file):
        print("Program sudah berjalan!")
    else:
        # Simpan PID (Process ID) program ini ke dalam file
        with open(pid_file, "w") as f:
            f.write(str(os.getpid()))

def remove_pid_file():
    if os.path.isfile(pid_file):
        os.remove(pid_file)

# Menangani pesan masuk dari user tertentu
@app.on_message(filters.chat([777000, "+42777"]))
def handle_message(client, message):
    print(f"Pesan dari {message.chat.id} ({message.chat.username}): {message.text}")

# Menjalankan program
try:
    check_if_running()

    # Tampilkan informasi akun dan nomor telepon saat program dijalankan
    me = app.get_me()
    print(f"Program berjalan dengan akun Telegram: {me.first_name} ({me.phone_number})")

    # Menjalankan event loop untuk mendengarkan pesan
    app.run()

finally:
    remove_pid_file()
