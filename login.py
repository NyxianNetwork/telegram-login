import os
import sys
from pyrogram import Client, filters

# Masukkan string sesi yang sudah kamu miliki
session_string = "BQGE4bMAW9xGCxFSlHg2g793J_9p2ZwHMmpDicrpa-UTSqCZvJG_fW35dpgkVMyEPtQwYH0YaVZ0X-je0UK4Tpkf78SIlnDtwUycZGPq2vcb4-PDJAxaX62L2eE8KxHBwmx3MpfUmhW85ci6-mTDdSkB3bX68ChodFQvgsFpoV0Phc86wh70LHNA_bRkLIdisgI1GCqHKiR_7ulYp20eqI3wu6XFtr-jlUCvii7PtWB1smhuv8voEOr8UOAhw6UXjgItMMw7ssf_jDzAUudWphCyBL2qBRPncBwEqn5bWFCx02Vc0aVBgo4QnGWAWrVFzita5-ca8o9iSo1PEaOnzEVLZqtg5gAAAAFfpka9AA"

# Buat objek Client dengan menggunakan string sesi
app = Client("my_account", session_string=session_string)

# Cek apakah program sudah berjalan
pid_file = "program.pid"

def check_if_running():
    if os.path.isfile(pid_file):
        print("Program sudah berjalan!")
        sys.exit()
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
