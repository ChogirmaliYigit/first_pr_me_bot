import logging

from aiogram import Bot, enums

from data.config import ADMINS


async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            bot_properties = await bot.me()
            message = ["*Bot ishga tushdi\.*\n",
                       f"*Bot ID:* {bot_properties.id}",
                       f"*Bot Username:* @{bot_properties.username}"]
            await bot.send_message(int(admin), "\n".join(message), parse_mode=enums.ParseMode.MARKDOWN_V2)
        except Exception as err:
            logging.exception(err)
