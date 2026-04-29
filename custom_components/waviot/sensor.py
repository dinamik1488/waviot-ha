from homeassistant.helpers.update_coordinator import CoordinatorEntity

UNIT_MAP = {
    "temperature": "°C",
    "battery": "V",
    "voltage": "V",
    "current": "A",
    "power": "kW",
    "energy": "kWh",
}

def guess_unit(key: str):
    key = key.lower()
    for k, unit in UNIT_MAP.items():
        if k in key:
            return unit
    return None


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["waviot"][entry.entry_id]

    entities = []

    modem = coordinator.data.get("modem", {})
    values = coordinator.data.get("values", {})

    # базовые сенсоры
    for key in ["temperature", "battery"]:
        if key in modem:
            entities.append(WaviotSensor(coordinator, key, "modem"))

    # все registrators автоматически
    for reg_id, reg_data in values.items():
        entities.append(WaviotSensor(coordinator, reg_id, "reg"))

    async_add_entities(entities)


class WaviotSensor(CoordinatorEntity):

    def __init__(self, coordinator, key, source):
        super().__init__(coordinator)
        self.key = key
        self.source = source

    @property
    def name(self):
        return f"WAVIoT {self.key}"

    @property
    def unique_id(self):
        return f"waviot_{self.key}"

    @property
    def state(self):
        data = self.coordinator.data

        if self.source == "modem":
            return data.get("modem", {}).get(self.key)

        if self.source == "reg":
            return data.get("values", {}).get(self.key, {}).get("last_value")

        return None

    @property
    def unit_of_measurement(self):
        return guess_unit(self.key)
