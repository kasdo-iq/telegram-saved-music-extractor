import os
import zipfile
import asyncio
from telethon import TelegramClient, events

# Credentials (user must fill these)
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE = 'YOUR_PHONE_NUMBER'

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
