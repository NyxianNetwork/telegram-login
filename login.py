from pyrogram import Client, filters
import time

# String sesi Telegram yang sudah kamu miliki
session_string = "BQAAxJIAKdW1LwjEFT-P2yLdVP04dC8czD3GH_wt1O0zZFEwemcMgwpfhLiOQPFaCCNqaCnbRd9Qek9xmmrFnkGFsSKN6D4_N40ltDpNxhDI2YOjJ1WCipYyOtJrKPqVcW--M1DzLtnnxN0jVxPLz8fqcJMxt6cU5vpPzh9Pq9uQIXGPTwAxZvr74tvsSUMyp_6v5fVeJCKQdXWgt7TFUZq8YqyuF782vknD4h3lXC-lTMda8gk4fHFIUBlWx_j5Yqv6pj637mPwGxYi54Q0wq-PS92z8eM6vtjtu1C9BYlYbd6BkPSQTETbUICNASUB_idCxQ4NAJTyXfEtXyXToO14trv1FwAAAAB8uUzXAA"

# Buat objek Client dengan menggunakan string sesi
app = Client("my_account", session_string=session_string)

# Menjalankan aplikasi dan menangani error
if __name__ == "__main__":
    try:
        app.start()  # Memulai Client
        me = app.get_me()  # Memanggil `get_me()` setelah Client dimulai
        print(f"Login sebagai: {me.first_name} ({me.phone_number})")

        print("Program sedang berjalan. Tekan CTRL + C untuk menghentikan.")
        app.run()  # Menjalankan event loop
    except pyrogram.errors.exceptions.not_acceptable_406.AuthKeyDuplicated:
        print("Session sedang digunakan di tempat lain. Silakan coba lagi nanti.")
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(f"Terjadi error yang tidak terduga: {e}")
    finally:
        try:
            app.stop()  # Menghentikan Client dengan aman
        except Exception as e:
            print(f"Terjadi kesalahan saat menghentikan Client: {e}")
        print("Program selesai.")

    # Tambahan untuk memastikan program tidak langsung keluar
    while True:
        time.sleep(1)
