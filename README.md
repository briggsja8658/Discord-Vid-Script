# Discord Vid Script
- High level
    * Looking to expose and immerse students in the world of technology passively. Being that I communicate with students on discord anyways. This was an opportunistic script to give students more discoverability to tech content
    * There was a mental health channel that was largely a failed experiment. However, its possible that student got value from it and didn't want to admit it.  


# Features
- Primary Goal
    * Catch new uploads and announce them in category-specific Discord channels (hardware, networking, programming, mental-health).

- Tracking
    * Stores last-seen video per channel in `discord_vid_state.json`.
    * Seeds a default channel list when the state file is empty.

- Notifications
    * Sends webhook messages with channel name and video link.
    * Uses category-specific avatars/colors from `pictures/`.


# Tech
- Script
    * Python 3
    * requests
    * google-api-python-client (YouTube Data API v3)
- Storage
    * Local JSON state file
    * Plain-text log file


# Prerequisites
- Python 3.9+ (or your preferred 3.x)
- pip
- YouTube Data API key
- Discord webhooks for each category


# Run the project
- Clone the repository (if not already cloned)
    * git clone `https://github.com/briggsja8658/Discord-Vid-Script.git`
    * cd Discord-Vid-Script
- Install dependencies
    * pip install `google-api-python-client` `requests`
- Configs
    * Update `config.py` with your Google API key and Discord webhook URLs.
    * Adjust `check_interval` (seconds) if you want a different polling rate.
    * Ensure `json_file_path` and `log_file` point to writable locations.
- Start
    * python `yt_discord.py`
- Logs
    * Check `log_file.txt` for run history and errors.


# Project structure (top-level)
- `yt_discord.py` — main polling loop and webhook posting
- `config.py` — runtime configuration (API key, webhooks, paths)
- `discord_vid_state.json` — persisted channel state
- `log_file.txt` — runtime logs
- `pictures/` — webhook avatar assets


# Notes
- Channels are referenced by YouTube handle via `forHandle`
    * Update `discord_vid_state.json` to add or remove channels.
- `config.py` is in `.gitignore` so keep your real keys local or load them from env if you refactor.
- The script runs continuously
    * Use a process manager or scheduled task if you need it to stay alive.
