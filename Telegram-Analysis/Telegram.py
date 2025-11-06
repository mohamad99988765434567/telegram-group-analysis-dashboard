from telethon import TelegramClient
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

api_id_str = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

if not api_id_str or not api_hash:
    raise RuntimeError("API_ID or API_HASH missing. Check your .env file")

api_id = int(api_id_str)

client = TelegramClient('my_session', api_id, api_hash)

groups = [
    "https://t.me/Ai_Arabic1",
    "https://t.me/dakasinaee",
    "https://t.me/pyt_ar"
]

MESSAGES_PER_CHAT = 1000

async def main():
    grouped_messages = {}

    for group in groups:
        entity = await client.get_entity(group)
        chat_title = getattr(entity, "title", str(group))

        messages = await client.get_messages(entity, limit=MESSAGES_PER_CHAT)
        grouped_messages[chat_title] = []

        for msg in messages:
            text = msg.message or ""
            author = None
            if msg.sender:
                if getattr(msg.sender, "username", None):
                    author = msg.sender.username
                elif getattr(msg.sender, "first_name", None):
                    author = msg.sender.first_name
                else:
                    author = str(msg.sender.id)

            grouped_messages[chat_title].append({
                "message_text": text,
                "timestamp": msg.date.isoformat() if msg.date else None,
                "author": author
            })

    with open("telegram_messages_by_group.json", "w", encoding="utf-8") as f:
        json.dump(grouped_messages, f, ensure_ascii=False, indent=2)

    print("Saved messages grouped by chat → telegram_messages_by_group.json")

with client:
    client.loop.run_until_complete(main())
