from dotenv import load_dotenv
import os, json
from telethon.sync import TelegramClient
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
channel_usernames = ["lobelia4cosmetics", "tikvahpharma","CheMed123"]

# Output paths
date_str = datetime.today().strftime("%Y-%m-%d")
base_path = Path(f"data/raw/telegram_messages/{date_str}")
base_path.mkdir(parents=True, exist_ok=True)

# Start Telegram client
with TelegramClient('anon', api_id, api_hash) as client:
    for username in channel_usernames:
        print(f"Scraping: {username}")
        messages = []
        try:
            for message in client.iter_messages(username, limit=100):
                messages.append(message.to_dict())

                # Download images only
                if message.photo:
                    image_path = base_path / f"{username}_{message.id}.jpg"
                    client.download_media(message, file=image_path)

            # Save messages to JSON
            out_path = base_path / f"{username}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2, default=str)

        except Exception as e:
            print(f"Failed scraping {username}: {e}")
