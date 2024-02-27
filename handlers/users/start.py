from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import db, bot
from data.config import ADMINS
from utils.extra_datas import make_title

router = Router()


@router.message(CommandStart(deep_link=True))
async def deep_linking(message: types.Message, command: CommandObject):
    user = await db.select_referral_by_user(user_id=message.from_user.id)
    if not user:
        await db.add_referral(referral=command.args, user_id=message.from_user.id)
    await do_start(message)


@router.message(CommandStart())
async def do_start(message: types.Message):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    user = None

    try:
        user = await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
    except Exception as error:
        logger.info(error)

    if user:
        count = await db.count_users()
        msg = f"[{make_title(user['full_name'])}](tg://user?id={user['telegram_id']}) added to db\.\nDb has {count} users\."
    else:
        msg = f"[{make_title(full_name)}](tg://user?id={telegram_id}) already added to db"

    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")

    await message.answer(
        f"Hi {make_title(full_name)}\!👋\n\nWhat's your Github username?🤔",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
