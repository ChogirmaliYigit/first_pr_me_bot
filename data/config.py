from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")

GITHUB_PR_URL = "https://api.github.com/search/issues?q=type:pr+author:%22{username}%22+-user:%22{username}%22&sort=created&order=asc&per_page=1"
GITHUB_USER_URL = "https://api.github.com/users/{username}"
