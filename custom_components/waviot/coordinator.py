from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta
from .api import WaviotAPI

class WaviotCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, modem_id, api_key):
        self.api = WaviotAPI(modem_id, api_key)

        super().__init__(
            hass,
            name="waviot",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        modem = await self.api.get_modem_info()
        values = await self.api.get_values()

        return {
            "modem": modem.get("modem", {}),
            "values": values.get("registrators", {})
        }
