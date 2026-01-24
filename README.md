## Setup

```bash
git clone https://github.com/paulvp/telegram-bot-example
cd telegram-bot-example

uv venv
source .venv/bin/activate

uv pip install -r requirements.txt

cp .env.example .env
# Edit .env with your bot token
```

## Usage

### Local Development

```bash
python3 bot.py
```

### Docker Deployment

**Run container:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the bot:**
```bash
docker-compose down
```

### Railway Deployment

1. **Deploy directly from GitHub:**
   - Go to [Railway](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables in Railway dashboard
   - Deploy

## Monitoring & Logs

**View logs:**
```bash
tail -f logs/bot.log
```

Logs include:
- `logs/bot.log` - Current day logs  
- `logs/bot.log.YYYY-MM-DD` - Historical logs (7 days retention)

## Troubleshooting

### Bot not starting
```bash
# Check logs
docker-compose logs -f

# Verify environment variables  
docker-compose config

# Restart container
docker-compose restart
```

## Links

- [aiogram Documentation](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Railway Documentation](https://docs.railway.app/)
- [Docker Documentation](https://docs.docker.com/)


MIT License

---

<p align="center">Made with ☕️</p>
