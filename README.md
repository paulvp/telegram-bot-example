# telegram-bot-example

## ✨ Features

- 🎉 **Message Effects**: Confetti, fire, heart, and other animated effects
- 🌐 **WebApp Integration**: Seamless Telegram Mini App support
- 🔒 **Security**: Rate limiting, input sanitization, callback validation
- 🐳 **Optimized Docker**: Multi-stage Alpine build (~50MB image)
- 🚀 **Railway Ready**: One-click deployment configuration
- 📊 **Logging**: Rotating file logs with console output
- 🔄 **Auto-restart**: Automatic recovery from crashes
- ⚡ **Performance**: Async/await patterns throughout

## 📋 Use Cases

### Perfect for:
## 🚀 Setup

```bash
git clone https://github.com/paulvp/telegram-bot-example
cd telegram-bot-example

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your bot token
```

## 📖 Usage

### Local Development (Easiest way!)

```bash
python3 bot.py
```

Your bot will start and be ready to receive messages!

### Docker Deployment

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

### Railway Deployment (One-click!)

1. **Deploy directly from GitHub:**
   - Go to [Railway](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables in Railway dashboard
   - Deploy! 🚀

2. **Or use Railway CLI:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway variables set TELEGRAM_BOT_TOKEN=your_token_here
railway variables set WEBAPP_URL=https://your-webapp.vercel.app/
railway up
```ectly from GitHub:
1. Push your code to GitHub
2. Go to [Railway](https://railway.app/)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables in Railway dashboard
6. Deploy! 🚀
```

## 📊 Monitoring & Logs

**View logs:**
```bash
tail -f logs/bot.log
```

Logs include:
- `logs/bot.log` - Current day logs  
- `logs/bot.log.YYYY-MM-DD` - Historical logs (7 days retention)

## 🔧 Troubleshooting

### Bot not starting
```bash
# Check logs
docker-compose logs -f

# Verify environment variables  
docker-compose config

# Restart container
docker-compose restart
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/CoolFeature`)
3. Commit your changes (`git commit -m 'Add CoolFeature'`)
4. Push to the branch (`git push origin feature/CoolFeature`)
5. Open a Pull Request

### Ideas for Contributions
- [ ] Multi-language support
- [ ] Advanced rate limiting
- [ ] Database integration
- [ ] Payment processing

## 🔗 Links

- [aiogram Documentation](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Railway Documentation](https://docs.railway.app/)
- [Docker Documentation](https://docs.docker.com/)

## 💬 Support

- Create an [Issue](https://github.com/paulvp/telegram-bot-example/issues)

## ⚠️ Security Notice

**NEVER commit your `.env` file with real tokens!**

Always use `.env.example` as a template and add `.env` to `.gitignore`.

## 📝 License

MIT License

---

<p align="center">Made with ☕️ and 🌃</p>
<p align="center"><sub>add ⭐</sub></p>
