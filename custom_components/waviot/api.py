import aiohttp

class WaviotAPI:

    def __init__(self, modem_id, api_key):
        self.modem_id = modem_id
        self.api_key = api_key

    async def get_modem(self):
        url = f"https://lk.waviot.ru/api.modem/info/?id={self.modem_id}&key={self.api_key}"
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                return await r.json()

    async def get_values(self):
        url = f"https://lk.waviot.ru/api.data/get_values/?modem_id={self.modem_id}&key={self.api_key}&limit=1"
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                return await r.json()
