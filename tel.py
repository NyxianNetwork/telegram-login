# tel.py
from telethon import TelegramClient
from telethon.sessions import StringSession

# ======= Masukkan API ID, API HASH, dan String Session di sini =======
api_id = 20958475      # Ganti dengan API ID kamu
api_hash = "1cfb28ef51c138a027786e43a27a8225"  # Ganti dengan API Hash kamu
string_session = "1BVtsOK0Bu3xN5xmFw_deShO6mWOxB7p4qAawR0O4Hdxgtx96G_slPazFYXNppoSh6XaYumTs1l7lwf9RTsJyMqx9lRUxgvbc8WCwPjemkRIaWwRmDvKbCPf8S5eBqCCVlrnD5mUUtbAt-nrNGczOIlC1bFzGrWbsW7_CERtKXo7K3F5vEspBoBCVwmrdGU_Yoj7JWRJoyErAmblt3_pFoxFifLRzo3HTRUYuIfU38lvpNsKZEN-J1sRHzca1XHPH8s0pwSxZ3hbdeJoMD_gNhNm-gka1wCcfGUejx9FetSHfaUBKkrs7Dlkq1p9aVh1jG2YE4pz6gjjMtBV7nDmsBC3o0oz4wM8="  # Ganti dengan String Session kamu
# =====================================================================

async def main():
    me = await client.get_me()
    print("=== Login Berhasil ===")
    print(f"Nama       : {me.first_name} {me.last_name or ''}")
    print(f"Username   : @{me.username}" if me.username else "Username   : (Tidak ada)")
    print(f"ID Telegram: {me.id}")
    print(f"Nomor HP   : {me.phone}")
    print("======================")

with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
    client.loop.run_until_complete(main())
