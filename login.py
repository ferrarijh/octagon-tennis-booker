import aiohttp
import getpass
import logging
from configs.config import *
from yarl import URL

logger = logging.getLogger(__name__)

async def login(session: aiohttp.ClientSession, url: str, email: str|None=None, password: str|None=None):
    while not email:
        email = input(f"Email: ")
        if not email:
            logger.warning("Email cannot be empty, try again.")

    while not password:
        password = getpass.getpass("Password: ")
        if not password:
            logger.warning("Password cannot be empty, try again.")

    data = {
        "email": email,
        "password": password,
    }

    async with session.post(url, data=data) as resp:
        # aiohttp also follows redirects by default
        # for h in resp.history:
        #     print("Redirect:", h.status, h.url, "Set-Cookie:", h.headers.get("Set-Cookie"))

        cookies = session.cookie_jar.filter_cookies(URL(url))
        auth_cookie = cookies.get(SESSION_COOKIE_NAME)

        if not auth_cookie:
            if resp.status == 200:
                logger.error("Login failed, please check your email/password")
            else:
                raise RuntimeError(f"Login failed. status={resp.status} .ASPXAUTH not found")
        else:
            logger.info("Login successful.")
            return