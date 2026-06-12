# Telegram Profile Music Extractor to ZIP

This script extracts all audio files (songs) from your **Telegram Profile Music Tab** (the "Save Music in Profile" feature) and compresses them into a single ZIP file.

## Features
- **Profile Music Extraction**: Specifically targets songs saved to your profile music tab.
- **Fallback Support**: If no profile music is found or the feature is not supported by your account, it falls back to scanning your "Saved Messages".
- **Auto-ZIP**: Automatically bundles all downloaded songs into a `.zip` archive.

## Requirements

Ensure you have the `telethon` library installed:

```bash
sudo pip3 install telethon
```

## How to Use

1.  **Get `API_ID` and `API_HASH`:**
    *   Go to [https://my.telegram.org/apps](https://my.telegram.org/apps).
    *   Log in and create an application to get your credentials.

2.  **Configure the Script:**
    *   Open `telegram_music_extractor.py`.
    *   Fill in your `API_ID`, `API_HASH`, and `PHONE`.

3.  **Run:**
    *   Execute the script:
        ```bash
        python3 telegram_music_extractor.py
        ```

4.  **Result:**
    *   A file named `profile_songs.zip` will be created containing all your profile songs.

---
*Note: This tool is for personal use to backup your own saved music.*
