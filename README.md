# Telegram Profile Music Extractor

A small Telethon script that downloads the audio saved to your Telegram **profile music tab** ("Save Music in Profile") and packs it into a single `profile_songs.zip`.

## What it does

The script logs in with your user account, requests the saved music IDs from your profile, resolves each ID to an audio message and downloads it into a temporary `profile_songs/` folder. When finished, it zips the folder and deletes the individual files.

If the profile-music request fails or your account/layer does not support it, the script falls back to scanning your **Saved Messages** for audio files.

## Features

- Profile music extraction through `account.GetSavedMusicIds`.
- Fallback scan of Saved Messages when profile music is unavailable.
- Automatic ZIP creation and cleanup of the temporary folder.
- Skips anything that is not an audio message.

## Requirements

- Python 3.10 or newer
- Telethon
- A Telegram account and API credentials from [my.telegram.org](https://my.telegram.org)

## Setup

```bash
git clone https://github.com/kasdo-iq/telegram-saved-music-extractor.git
cd telegram-saved-music-extractor
python -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install telethon
```

Open `telegram_music_extractor.py` and replace the three placeholders at the top:

```python
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE = 'YOUR_PHONE_NUMBER'
```

On the first run Telethon asks for the login code (and the 2FA password if enabled) and creates `session_name.session` in the working directory.

## Usage

```bash
python telegram_music_extractor.py
```

The script prints progress for each song and writes the archive to the current directory:

```text
profile_songs.zip
```

If no songs are found, nothing is downloaded and the temporary folder is removed.

## Configuration

All configuration is at the top of `telegram_music_extractor.py`; there is no `.env` file.

| Setting | Description |
|---|---|
| `API_ID` | API ID from my.telegram.org. |
| `API_HASH` | API hash from my.telegram.org. |
| `PHONE` | Phone number in international format, used for the first login. |

Runtime files:

- `session_name.session` — login session. **Secret**; it grants access to the account.
- `profile_songs/` — temporary downloads, removed after zipping.
- `profile_songs.zip` — the output archive.

All three are covered by `.gitignore`.

## Project structure

```text
telegram-saved-music-extractor/
├── telegram_music_extractor.py   # the whole tool
├── README.md
└── .gitignore
```

## Verification

There are no automated tests. A syntax check without credentials:

```bash
python -m compileall -q telegram_music_extractor.py
```

## Limitations

- The profile-music API is relatively new. On older Telethon versions or account layers the request may fail, and the script then falls back to **all audio in Saved Messages**, which can include files that are not profile music.
- The output file name is fixed (`profile_songs.zip`); running the script twice in the same folder overwrites the earlier archive.
- Downloaded files are deleted after zipping, so keep the ZIP if you want a backup.

## Responsible use

- Use this only with your own account and your own saved music.
- Music files are copyrighted. Do not redistribute the archive or use it to build a public library.
- Keep the session file private and never commit it.
