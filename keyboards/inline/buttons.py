from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.switch_inline_query_chosen_chat import SwitchInlineQueryChosenChat


inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def make_share_markup(inline_query: str, url: str, pr_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Share on Telegram",
                    switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(
                        query=inline_query,
                        allow_bot_chats=True,
                        allow_group_chats=True,
                        allow_channel_chats=True,
                        allow_user_chats=True,
                    ),
                ),
                InlineKeyboardButton(
                    text="Share on X",
                    url=f"https://twitter.com/intent/tweet?"
                        f"original_referer={url}"
                        f"&text=I%20found%20my%20%23FirstPullRequest%3A%20{pr_link}.%20What%20was%20yours%3F"
                        f"&url={url}",
                ),
            ],
        ],
    )
