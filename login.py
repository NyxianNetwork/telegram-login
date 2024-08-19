from pyrogram import Client, filters
import time

# String sesi Telegram yang sudah kamu miliki
session_string = "AQFFwxoAwX35DhN5Wq7p9tp6JJsdaGYuYJXBPj-MaEKn5nqWLlkPZ84nfkSpSTo997P5l5k7j6NqeqthZXwzthUFCl9ucgrxXCzvPayoxA75a4JehVbrztoRn9rH7Opb92wFs3dacOiJAqlNiAZ0WjsVgPVlg8iCRQUOy5OSCnGf6BfJlBTXOmnwFxmpJur7JJglSEFYo01s1zfctVPZ-nM7AzsZzsYN_nw3_HoUc4TFmwfMxe8xuzJ6w0b6ahqnUERjgly7A3CjKy7lw7vz1LTeDXmAjbkkVkH5nkOC0dbivUmDKV53llm2DzmFV2Wm6YqkxJv_FKXbxRZE2lpDePayk_UuIgAAAABs_9IyAA"

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
