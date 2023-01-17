import aiohttp


class ClearBitAPIClient:
    """Клиент Clearbit.com"""
    # api_key = 'sk_a6c90a3b2e50ee1dce8546148f1d06e1' # благополучно стырил ключ с просторов GitHub'а)))
    # api_key = 'sk_9bf01725057a2b54533f372ec91f46d1' # благополучно стырил ключ с просторов GitHub'а)))
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get(self, url: str, params: dict):
        async with aiohttp.request(method='GET', url=url, params=params, headers={'Authorization': f'Bearer {self.api_key}'}) as resp:
            return await resp.json()

    async def enrichment_find(self, email: str):
        return await self.get(url='https://person.clearbit.com/v2/combined/find', params={'email': email})
