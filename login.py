import os
from pyrogram import Client, filters

# Masukkan string sesi Telegram kamu di sini
session_string = "BQGE4bMAW9xGCxFSlHg2g793J_9p2ZwHMmpDicrpa-UTSqCZvJG_fW35dpgkVMyEPtQwYH0YaVZ0X-je0UK4Tpkf78SIlnDtwUycZGPq2vcb4-PDJAxaX62L2eE8KxHBwmx3MpfUmhW85ci6-mTDdSkB3bX68ChodFQvgsFpoV0Phc86wh70LHNA_bRkLIdisgI1GCqHKiR_7ulYp20eqI3wu6XFtr-jlUCvii7PtWB1smhuv8voEOr8UOAhw6UXjgItMMw7ssf_jDzAUudWphCyBL2qBRPncBwEqn5bWFCx02Vc0aVBgo4QnGWAWrVFzita5-ca8o9iSo1PEaOnzEVLZqtg5gAAAAFfpka9AA"

# Buat objek Client dengan menggunakan string sesi
app = Client("my_account", session_string=session_string)

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

# Menangani pesan masuk dari nomor +42777 atau ID 777000
@app.on_message(filters.chat([777000, "+42777"]))
def handle_message(client, message):
    print(f"Pesan dari {message.chat.id} ({message.chat.username}): {message.text}")

# Menjalankan program
try:
    check_if_running()

    with app:
        # Dapatkan informasi akun yang sedang login
        me = app.get_me()

        # Coba dapatkan nomor telepon (jika tersedia)
        phone_number = me.phone_number if me.phone_number else "Nomor telepon tidak tersedia"

        print(f"Nama: {me.first_name} {me.last_name if me.last_name else ''}")
        print(f"Username: @{me.username}")
        print(f"Nomor Telepon: {phone_number}")

        print("Menunggu pesan masuk...")

        # Menjalankan event loop untuk mendengarkan pesan
        app.run()

finally:
    remove_pid_file()
