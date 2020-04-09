## Male' Map TelegramBot

A simple TelegramBot to fetch residential addresses in Male', Maldives. The bot can be queried inline or directly.

### sample `.env` file

```bash
DEBUG=true
SQLITE_SOURCE=databases/maalemap.db
MAPBOT_API_TOKEN=YOURBOTTOKEN

# enable webhook support
WEBHOOK=false

# these are for webhook config
WEBHOOK_PORT=80
WEBHOOK_URL=https://yourwebhookurl.herokuapp.com
WEBHOOK_PATH=/maalemaps/bot
```