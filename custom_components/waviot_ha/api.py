import aiohttp
import time

class WaviotAPI:
    def __init__(self, modem_id, api_key):
        self.modem_id = modem_id
        self.api_key = api_key

    async def get_data(self):
        now = int(time.time())
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://lk.waviot.ru/api.data/get_values/?modem_id={self.modem_id}&key={self.api_key}&from={now-3600}&to={now}&limit=1"
            ) as r:
                return await r.json()
