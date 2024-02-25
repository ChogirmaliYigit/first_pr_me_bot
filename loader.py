from aiogram import Bot
from utils.db.postgres import Database
from data.config import BOT_TOKEN

db = Database()
bot = Bot(token=BOT_TOKEN)
