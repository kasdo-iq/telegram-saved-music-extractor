import os
import zipfile
import asyncio
from telethon import TelegramClient, functions, types

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
    download_path = 'profile_songs'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print("Fetching songs from your Profile (Save Music in Profile)...")
    
    songs_count = 0
    
    try:
        # Step 1: Get all saved music IDs from the profile
        # Note: account.getSavedMusicIds is a relatively new method in Layer 214+
        saved_music_ids_result = await client(functions.account.GetSavedMusicIdsRequest(hash=0))
        
        if hasattr(saved_music_ids_result, 'ids') and saved_music_ids_result.ids:
            music_ids = saved_music_ids_result.ids
            print(f"Found {len(music_ids)} songs in your profile.")
            
            # Step 2: Fetch the actual document objects using the IDs
            # We can use messages.getMessages for this as it can return messages/media by ID
            # However, for profile music, these are often documents.
            # A more robust way in Telethon is to fetch the 'Full User' info which might contain some
            # but for a list, we might need to iterate or use specific methods.
            
            # Since these IDs refer to messages/documents in the 'Saved Messages' but flagged for profile
            # or specifically stored as documents, we will try to fetch them.
            
            for doc_id in music_ids:
                # We try to get the document. In Telethon, we can use GetMessagesRequest 
                # but usually, we need the peer. For profile music, it's usually the user themselves.
                try:
                    # Fetching the document via GetMessagesRequest with 'me' as peer
                    messages = await client(functions.messages.GetMessagesRequest(id=[types.InputMessageID(id=int(doc_id))]))
                    
                    for msg in messages.messages:
                        if isinstance(msg, types.Message) and msg.audio:
                            file_name = msg.file.name or f"profile_song_{msg.id}.mp3"
                            print(f"Downloading: {file_name}")
                            
                            path = await client.download_media(msg, file=os.path.join(download_path, file_name))
                            if path:
                                songs_count += 1
                except Exception as e:
                    print(f"Error processing song ID {doc_id}: {e}")
        else:
            print("No songs found in your profile music tab.")

    except Exception as e:
        print(f"An error occurred while fetching profile music: {e}")
        print("Falling back to searching 'Saved Messages' generally...")
        # Fallback to the previous method if the new API method fails or isn't supported
        async for message in client.iter_messages('me'):
            if message.audio:
                file_name = message.file.name or f"song_{message.id}.mp3"
                print(f"Downloading (Fallback): {file_name}")
                path = await message.download_media(file=os.path.join(download_path, file_name))
                if path:
                    songs_count += 1

    if songs_count > 0:
        print(f"Downloaded {songs_count} songs. Creating ZIP file...")
        
        zip_filename = 'profile_songs.zip'
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(download_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    zipf.write(full_path, os.path.relpath(full_path, download_path))
                    os.remove(full_path)
        
        os.rmdir(download_path)
        print(f"Done! The file is ready as: {zip_filename}")
    else:
        print("No songs were downloaded.")
        if os.path.exists(download_path):
            os.rmdir(download_path)

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
