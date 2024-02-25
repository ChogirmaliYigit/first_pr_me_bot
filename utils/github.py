import aiohttp
from humanize import naturaltime
from datetime import datetime
from data import config
from utils.extra_datas import make_title
from loader import db
from keyboards.inline.buttons import make_share_markup


async def get_first_pr(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(config.GITHUB_USER_URL.format(username=username)) as user_response:
            data = await user_response.json()
            if data.get("message") == "Not Found":
                return None, f"*{username}* doesn't appear to be on GitHub at all\.", None, None

        async with session.get(config.GITHUB_PR_URL.format(username=username)) as pr_response:
            response = await pr_response.json()
            if not response.get("items", None):
                return None, f"It doesn't look like *{username}* has sent a pull request yet\.", None, None

            detail = response["items"][0]
            number = detail["number"]
            title = make_title(detail["title"])
            pull_request = detail["pull_request"]
            html_url = pull_request["html_url"]
            user = detail["user"]
            login = make_title(user["login"])
            user_html_url = make_title(user["html_url"])
            avatar_url = user["avatar_url"]
            existing_image = await db.select_image_by_link(avatar_url)
            if existing_image:
                image = existing_image.get("file_id")
            else:
                image = avatar_url

            pr_to = make_title(html_url.split('/')[3] + "/" + html_url.split('/')[4])
            pr_to_link = make_title("https://github.com/" + pr_to)

            async with session.get(pull_request["url"]) as pr_data:
                pr_info = await pr_data.json()
                pr_status = pr_info["state"]

            date = detail["created_at"].split("-")
            year, month, day = date[0], date[1], date[2][:2]
            pr_time = naturaltime(datetime(int(year), int(month), int(day)))

            message = (f"*[{title}]({make_title(html_url)})* *\#{number}*\n"
                       f"To: [*{pr_to}*]({pr_to_link})\n"
                       f"[*{login}*]({user_html_url}) sent this pull request _{pr_time}_\n\n"
                       f">\#{pr_status.title()}**")

            return (
                image,
                message,
                login,
                await make_share_markup(
                    login,
                    "https://t.me/firstprmebot",
                    html_url,
                ),
            )
