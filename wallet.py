import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()
chat='@'

async def main() -> None:
    app = TelegramClient('my_account', os.getenv('API_ID'), os.getenv('API_HASH'))

    @app.on(events.NewMessage(chats=chat, incoming=True))
    async def handle_private_message(message):
        if message.buttons:
            for button in message.buttons:
                url = button[0].url
                if url.startswith("https://t.me/wallet?start="):
                    code = url.split("=")[1]
                    await app.send_message('@wallet', f'/start {code}')
    
    await app.start()
    await app.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())