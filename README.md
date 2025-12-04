# X → Discord Filter Bot

Polls tweets from a given X account, filters by keywords, and posts matches to Discord.

## Setup

1. Create a Discord webhook in your target channel.
2. Get X API Bearer Token and target account's numeric USER_ID.
3. Set environment variables in Render:
   - `X_BEARER_TOKEN`
   - `X_USER_ID`
   - `DISCORD_WEBHOOK`
4. Deploy as a Background Worker.