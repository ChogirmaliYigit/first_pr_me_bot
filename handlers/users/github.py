from aiogram import Router, types
from aiogram.enums.parse_mode import ParseMode
from utils.github import get_first_pr
from loader import db


router = Router()


@router.message()
async def start_user(message: types.Message):
    waiting = await message.answer("⏳")
    image, msg, inline_query, reply_markup = await get_first_pr(message.text)
    if image:
        msg = await message.answer_photo(
            image,
            msg,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=reply_markup,
        )

        file_id = msg.photo[-1].file_id
        existing_image = await db.select_image_by_file_id(file_id)
        if not existing_image:
            await db.add_image(file_id, image)
    else:
        await message.answer(
            msg,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
    await waiting.delete()


@router.inline_query()
async def get_username_inline(inline_query: types.InlineQuery):
    image, msg, username, reply_markup = await get_first_pr(inline_query.query)

    if image:
        results = [
            types.InlineQueryResultPhoto(
                id="1",
                photo_url=image,
                thumbnail_url=image,
                title=username,
                caption=msg,
                description=msg,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup,
            ),
        ]
    else:
        results = [
            types.InlineQueryResultArticle(
                id="1",
                title=username,
                input_message_content=types.InputTextMessageContent(
                    message_text=msg,
                    parse_mode=ParseMode.MARKDOWN_V2,
                    disable_web_page_preview=True,
                ),
                reply_markup=reply_markup,
                description=msg,
            ),
        ]

    await inline_query.answer(
        results=results,
    )
