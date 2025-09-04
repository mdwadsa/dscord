import os
import json
import asyncio
from datetime import datetime, timezone
from typing import Dict


import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv


# -------------------- IDs from the user --------------------
LOGIN_CHANNEL_ID = 1413017306698874951 # channel to accept !login/!logout
LIST_CHANNEL_ID = 1413017747394396191 # channel to show the list
TARGET_ROLE_ID = 1413017853338189895 # role to list holders (also staff for tickets)
OWNER_USER_ID = 948531215252742184 # allowed to run !setuppp


TICKETS_CATEGORY_NAME = "Tickets"
DATA_FILE = "logins.json"


# -------------------- Setup bot --------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True


bot = commands.Bot(command_prefix="!", intents=intents)


# -------------------- Persistence helpers --------------------


def now_utc() -> datetime:
return datetime.now(timezone.utc)


def load_data() -> Dict[str, str]:
if not os.path.exists(DATA_FILE):
return {}
try:
with open(DATA_FILE, "r", encoding="utf-8") as f:
raw = json.load(f)
# Expect {str(user_id): iso_timestamp}
return {k: v for k, v in raw.items() if isinstance(v, str)}
except Exception:
return {}




def save_data(data: Dict[int, datetime]):
pass

