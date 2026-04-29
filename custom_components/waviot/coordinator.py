from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta
from .api import WaviotAPI

class WaviotCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, modem_id, api_key):
        self.api = WaviotAPI(modem_id, api_key)
        super().__init__(hass, name="waviot", update_interval=timedelta(seconds=120))

    async def _async_update_data(self):
        return {"data": await self.api.get_data()}
