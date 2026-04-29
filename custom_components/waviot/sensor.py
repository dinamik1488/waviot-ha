from homeassistant.helpers.update_coordinator import CoordinatorEntity

SENSORS = ["temperature", "battery"]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["waviot"][entry.entry_id]

    async_add_entities([
        WaviotSensor(coordinator, key) for key in SENSORS
    ])


class WaviotSensor(CoordinatorEntity):

    def __init__(self, coordinator, key):
        super().__init__(coordinator)
        self.key = key

    @property
    def name(self):
        return f"WAVIoT {self.key}"

    @property
    def unique_id(self):
        return f"waviot_{self.key}"

    @property
    def state(self):
        return (
            self.coordinator.data.get("modem", {}).get(self.key)
        )
