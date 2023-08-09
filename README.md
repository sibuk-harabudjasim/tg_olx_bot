# TG_OLX_BOT - Telegram bot for parsing Olx.pl, Otomoto.pl and Gumtree.pl

This is hobby project that works better that search subscription on Olx.pl and probably as missing feature on other declared classifieds.
It is usually accessible at https://t.me/gmtree_bot when I'm willing to pay for DigitalOcean :). Ping me if you need it, or just deploy it by yourself.

# Usage

Go to https://t.me/gmtree_bot, start talking to bot with `/start`. Use buttons and read instructions in messages. Hope inteface will be intuitive.

# Installation

There was a way to deploy bot to Heroku, but it will take me a time to restore and add it to instruction. For now raw python deployment is available. Dockerfile pull requests are highly appreciated.

Requirements:
 - Python 3.11 (made so recent refactor, sorry, keep up with python versions)
 - Postgresql DB (probably will run with sqlite also, but for now it is basing on asyncpg)
 - requirements.txt
 - venv (optional, but let's keep out workplace clean :))

Steps:
```bash
# Clone repo
git clone ....
cd tg_olx_bot
# Install venv
python3 -m venv .venv
source .venv/bin/activate
# Install requirements
pip install -r requirements.txt
# Copy and fill .env file with telegram token, database dsn, etc
cp .env.example .env
vi .env
# Create database schema (customize db access as you need), pass password on prompt
psql -h localhost -U postgres -d postgres -f db_schema.sql
# Start bot
python run.py
```

# Troubleshooting

There are some logs available, just set DEBUG=1 in `.env`.
Also there are some testing utilities: `test_ad_parser.py` and `test_task.py`. They probably have some help messages and example payloads but can be outdated, so please dedicate some time to run it. Good luck.
