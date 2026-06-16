# BlueSky Bot

A safe Python automation project using the BlueSky/AT Protocol client. The bot can authenticate, read timeline posts, filter posts by keyword and interact with matching posts.

## Key skills

- Python scripting
- API authentication
- Environment variables
- Social platform API usage
- Automation logic
- Timeline/feed data processing

## Safety note

Do not hard-code usernames, passwords or API keys in source code. This version reads credentials from environment variables.

## Setup

```bash
pip install -r requirements.txt
export BLUESKY_USERNAME='your-handle.bsky.social'
export BLUESKY_PASSWORD='your-app-password'
python bluesky_bot.py
```

Use a BlueSky app password rather than your main account password.
