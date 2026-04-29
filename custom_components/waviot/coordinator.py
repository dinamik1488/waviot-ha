import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .api import WaviotAPI

_LOGGER = logging.getLogger(__name__)

class WaviotCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, modem_id, api_key):
        self.api = WaviotAPI(modem_id, api_key)

        super().__init__(
            hass,
            logger=_LOGGER,
            name="waviot",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        modem = await self.api.get_modem()
        values = await self.api.get_values()

        return {
            "modem": modem.get("modem", modem),
            "values": values.get("registrators", values.get("values", {}))
        }
