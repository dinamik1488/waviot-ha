from homeassistant.helpers.update_coordinator import CoordinatorEntity

SENSORS = {
    "temperature": "°C",
    "battery": "V",
    "power_active": "kW",
    "voltage_l1": "V",
    "voltage_l2": "V",
    "voltage_l3": "V",
    "current_l1": "A",
    "current_l2": "A",
    "current_l3": "A",
    "electricity_total": "kWh",
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["waviot"][entry.entry_id]

    async_add_entities(
        [WaviotSensor(coordinator, k) for k in SENSORS]
    )

class WaviotSensor(CoordinatorEntity):

    def __init__(self, coordinator, key):
        super().__init__(coordinator)
        self.key = key

    @property
    def unique_id(self):
        return f"waviot_{self.key}"

    @property
    def name(self):
        return f"WAVIoT {self.key}"

    @property
    def state(self):
        try:
            return (
                self.coordinator.data["modem"].get(self.key)
                or self.coordinator.data["values"].get(self.key, {}).get("last_value")
            )
        except:
            return None

    @property
    def unit_of_measurement(self):
        return SENSORS[self.key]