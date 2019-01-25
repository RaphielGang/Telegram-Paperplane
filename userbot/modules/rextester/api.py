import aiohttp

from userbot.modules.rextester.langs import languages


class Rextester(object):
    def __init__(self, lang, code, stdin):
        self.lang = lang
        self.code = code
        self.stdin = stdin
        self._test = None

    async def fetch(self, session, url, data):
        async with session.get(url, data=data) as response:
            return await response.json()

    async def exec(self):
        if self.lang not in languages:
            raise UnknownLanguage("Unknown Language")

        data = {
            "LanguageChoice": languages[self.lang],
            "Program": self.code,
            "Input": self.stdin}

        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, "https://rextester.com/rundotnet/api", data)
            self.result = response["Result"]
            self.warnings = response["Warnings"]
            self.errors = response["Errors"]
            self.stats = response["Stats"]
            self.files = response["Files"]
        return self


class UnknownLanguage(Exception):
    pass
