## Male' Map TelegramBot

A simple TelegramBot to fetch residential addresses in Male', Maldives. The bot can be queried inline or directly.

### sample `.env` file

```bash
DEBUG=true
SQLITE_SOURCE=databases/maalemap.db
MAPBOT_API_TOKEN=yourbotkeyfrombotfather

# enable webhook support [full hook will be {WEBHOOK_URL}{WEBHOOK_PATH}]
WEBHOOK=true
WEBHOOK_URL=https://yourwebhook.com
WEBHOOK_PATH=/bot

# local service for aiohttp listener
WEBAPP_HOST=0.0.0.0
WEBAPP_PORT=8443
```