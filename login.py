from pyrogram import Client, filters

# String sesi Telegram yang sudah kamu miliki
session_string = "AQFFwxoAwX35DhN5Wq7p9tp6JJsdaGYuYJXBPj-MaEKn5nqWLlkPZ84nfkSpSTo997P5l5k7j6NqeqthZXwzthUFCl9ucgrxXCzvPayoxA75a4JehVbrztoRn9rH7Opb92wFs3dacOiJAqlNiAZ0WjsVgPVlg8iCRQUOy5OSCnGf6BfJlBTXOmnwFxmpJur7JJglSEFYo01s1zfctVPZ-nM7AzsZzsYN_nw3_HoUc4TFmwfMxe8xuzJ6w0b6ahqnUERjgly7A3CjKy7lw7vz1LTeDXmAjbkkVkH5nkOC0dbivUmDKV53llm2DzmFV2Wm6YqkxJv_FKXbxRZE2lpDePayk_UuIgAAAABs_9IyAA"

# Buat objek Client dengan menggunakan string sesi
app = Client("my_account", session_string=session_string)

# Handler untuk menerima pesan dari nomor +42777 atau ID 777000
@app.on_message(filters.chat(["+42777", 777000]))
def receive_message(client, message):
    print(f"Menerima pesan dari {message.chat.id}: {message.text}")

# Menjalankan aplikasi dan menangani KeyboardInterrupt
if __name__ == "__main__":
    try:
        print("Program sedang berjalan. Tekan CTRL + C untuk menghentikan.")
        app.run()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
