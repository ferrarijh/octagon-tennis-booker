import aiohttp
import getpass
from constants import *
from yarl import URL

async def login(session: aiohttp.ClientSession, url: str):
    while True:
        email = input(f"Email (default is {EMAIL_DEFAULT}): ")
        if not email:
            email = EMAIL_DEFAULT
        while True:
            pw = getpass.getpass("Password: ")
            if pw:
                break
            print("Password cannot be empty, try again.")
        data = {
            "email": email,
            "password": pw,
        }

        async with session.post(url, data=data) as resp:
            # aiohttp also follows redirects by default
            # for h in resp.history:
            #     print("Redirect:", h.status, h.url, "Set-Cookie:", h.headers.get("Set-Cookie"))

            cookies = session.cookie_jar.filter_cookies(URL(url))
            auth_cookie = cookies.get(SESSION_COOKIE_NAME)

            if not auth_cookie:
                if resp.status == 200:
                    print("Login failed, please check your email/password")
                else:
                    raise RuntimeError(f"Login failed. status={resp.status} .ASPXAUTH not found")
            else:
                print("Login successful.")
                return