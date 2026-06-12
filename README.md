# Telegram Saved Music Extractor to ZIP

This script extracts all audio files (songs) from your Telegram Saved Messages and compresses them into a single ZIP file.

## Requirements

Ensure you have the `telethon` library installed:

```bash
sudo pip3 install telethon
```

## Code

Save the following code in a file named `telegram_music_extractor.py`:

```python
import os
import zipfile
import asyncio
from telethon import TelegramClient, events

# Credentials (user must fill these)
# You can get API_ID and API_HASH from https://my.telegram.org/apps
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE = 'YOUR_PHONE_NUMBER' # Your phone number with country code (e.g., +12345678900)

async def main():
    # Create the client
    client = TelegramClient('session_name', API_ID, API_HASH)
    
    print("Connecting to Telegram...")
    await client.start(phone=PHONE)
    print("Successfully logged in!")

    # Create a temporary folder for songs
    download_path = 'temp_songs'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print("Starting to search for songs in Saved Messages...")
    
    songs_count = 0
    # Get messages from Saved Messages
    # In Telegram, Saved Messages is a chat with "me"
    async for message in client.iter_messages('me'):
        # Check if the message contains an audio file
        if message.audio:
            file_name = message.file.name or f"song_{message.id}.mp3"
            print(f"Downloading: {file_name}")
            
            # Download the file to the temporary folder
            try:
                path = await message.download_media(file=os.path.join(download_path, file_name))
                if path:
                    songs_count += 1
            except Exception as e:
                print(f"Error downloading {file_name}: {e}")

    if songs_count > 0:
        print(f"Downloaded {songs_count} songs. Creating ZIP file...")
        
        zip_filename = 'saved_songs.zip'
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(download_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    zipf.write(full_path, os.path.relpath(full_path, download_path))
                    # Delete the file after adding it to the ZIP to save space
                    os.remove(full_path)
        
        # Delete the temporary folder
        os.rmdir(download_path)
        print(f"Done! The file is ready as: {zip_filename}")
    else:
        print("No songs found in Saved Messages.")
        if os.path.exists(download_path):
            os.rmdir(download_path)

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
```

## How to Use

1.  **Get `API_ID` and `API_HASH`:**
    *   Go to [https://my.telegram.org/apps](https://my.telegram.org/apps).
    *   Log in using your phone number.
    *   Click on "API development tools".
    *   Create a new application if you don't have one already. You will get your `API_ID` and `API_HASH`.

2.  **Modify the Code:**
    *   Open the `telegram_music_extractor.py` file.
    *   Replace `YOUR_API_ID` with your actual `API_ID`.
    *   Replace `YOUR_API_HASH` with your actual `API_HASH`.
    *   Replace `YOUR_PHONE_NUMBER` with your Telegram registered phone number, including the country code (e.g., `+12345678900`).

3.  **Run the Code:**
    *   Open a terminal in the same directory where you saved the file.
    *   Run the code using the command:
        ```bash
        python3 telegram_music_extractor.py
        ```
    *   The first time you run it, the script will ask you to enter the verification code you receive on Telegram.

4.  **Results:**
    *   After the execution is complete, you will find a file named `saved_songs.zip` in the same directory where you ran the script. This file contains all the songs extracted from your Saved Messages.

**Important Note:** This script will delete the temporary audio files after compressing them into a ZIP file to save storage space. Make sure you have backups of any important files before running the script if you are concerned about this.
