# tel.py
from telethon import TelegramClient
from telethon.sessions import StringSession

# === Data login (JANGAN bagikan ke orang lain) ===
api_id = 20958475
api_hash = '1cfb28ef51c138a027786e43a27a8225'
string_session = "1BVtsOK0Bu3xN5xmFw_deShO6mWOxB7p4qAawR0O4Hdxgtx96G_slPazFYXNppoSh6XaYumTs1l7lwf9RTsJyMqx9lRUxgvbc8WCwPjemkRIaWwRmDvKbCPf8S5eBqCCVlrnD5mUUtbAt-nrNGczOIlC1bFzGrWbsW7_CERtKXo7K3F5vEspBoBCVwmrdGU_Yoj7JWRJoyErAmblt3_pFoxFifLRzo3HTRUYuIfU38lvpNsKZEN-J1sRHzca1XHPH8s0pwSxZ3hbdeJoMD_gNhNm-gka1wCcfGUejx9FetSHfaUBKkrs7Dlkq1p9aVh1jG2YE4pz6gjjMtBV7nDmsBC3o0oz4wM8="

async def show_account_info():
    me = await client.get_me()
    print("\n=== Login Berhasil ===")
    print(f"Nama       : {me.first_name} {me.last_name or ''}")
    print(f"Username   : @{me.username}" if me.username else "Username   : (Tidak ada)")
    print(f"ID Telegram: {me.id}")
    print(f"Nomor HP   : {me.phone}")
    print("======================\n")

async def show_last_5_messages():
    print("\n=== 5 Pesan Terbaru dari 777000 ===")
    async for message in client.iter_messages(777000, limit=5):
        print(f"- [{message.date.strftime('%Y-%m-%d %H:%M:%S')}] {message.text}")
    print("===================================\n")

async def main():
    await show_account_info()
    
    while True:
        command = input("Masukkan perintah (1 = lihat pesan 777000, q = keluar): ").strip().lower()
        if command == "1":
            await show_last_5_messages()
        elif command == "q":
            print("Keluar dari program.")
            break
        else:
            print("Perintah tidak dikenal!")

with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
    client.loop.run_until_complete(main())
