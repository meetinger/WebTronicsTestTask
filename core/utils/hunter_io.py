import aiohttp

class HunterIOClient:
    # api_key = 'eb3697c6ff0dbc8d3167e5754aa304f6afbff5f7'  # благополучно стырил ключ с просторов GitHub'а)))
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get(self, url: str, params: dict):
        async with aiohttp.request(method='GET', url=url, params=params | {'api_key': self.api_key}) as resp:
            return await resp.json()

    async def verify_email(self, email: str):
        return await self.get(url='https://api.hunter.io/v2/email-verifier/', params={'email': email})
