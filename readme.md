## Male' Map TelegramBot

A simple TelegramBot to fetch residential addresses in Male', Maldives. The bot can be queried inline or directly.

### sample `.env` file

```bash
DEBUG=false
SQLITE_SOURCE=databases/maalemap.db

MAPBOT_API_TOKEN=telegramtoken
MAPBOT_API_TOKEN_VIBER=vibertoken

# enable webhook support
WEBHOOK_URL=https://google.com
WEBHOOK_PATH=/maalemaps/bot

# local service
WEBAPP_HOST=0.0.0.0
#WEBAPP_PORT=8443
```

## Testing
for testing webhooks, uncomment the following lines

```python
from pyngrok import ngrok
WEBHOOK_URL = ngrok.connect(WEBAPP_PORT).replace("http", "https").rstrip("/")
```