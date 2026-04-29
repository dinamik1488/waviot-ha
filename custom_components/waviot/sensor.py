from homeassistant.helpers.update_coordinator import CoordinatorEntity
from datetime import datetime

UNIT_MAP = {
    "temperature": "°C",
    "battery": "V",
    "voltage": "V",
    "current": "A",
    "power": "kW",
    "energy": "kWh",
}


def guess_unit(key):
    for k, v in UNIT_MAP.items():
        if k in key.lower():
            return v
    return None


async def async_setup_entry(hass, entry, async_add_entities):

    data = hass.data["waviot"][entry.entry_id]
    coordinator = data["coordinator"]

    entities = []

    modem = coordinator.data.get("modem", {})
    values = coordinator.data.get("values", {})

    # базовые
    for key in ["temperature", "battery"]:
        if key in modem:
            entities.append(WaviotSensor(coordinator, key, entry.entry_id))

    # все регистраторы
    for reg_id in values:
        entities.append(WaviotSensor(coordinator, reg_id, entry.entry_id))

    # ₽ сенсор
    entities.append(WaviotCostSensor(coordinator, entry.entry_id))

    async_add_entities(entities)


class WaviotSensor(CoordinatorEntity):

    def __init__(self, coordinator, key, entry_id):
        super().__init__(coordinator)
        self.key = key
        self.entry_id = entry_id

    @property
    def name(self):
        return f"WAVIoT {self.key}"

    @property
    def unique_id(self):
        return f"waviot_{self.key}"

    @property
    def state(self):

        data = self.coordinator.data

        return (
            data.get("modem", {}).get(self.key)
            or data.get("values", {}).get(self.key, {}).get("last_value")
        )

    @property
    def unit_of_measurement(self):
        return guess_unit(self.key)


class WaviotCostSensor(CoordinatorEntity):

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self.entry_id = entry_id

    @property
    def name(self):
        return "WAVIoT Energy Cost"

    @property
    def unique_id(self):
        return f"waviot_cost_{self.entry_id}"

    @property
    def state(self):

        data = self.coordinator.data
        hass_data = self.hass.data["waviot"][self.entry_id]

        energy = data.get("modem", {}).get("energy", 0)

        tariff_day = hass_data["tariff_day"]
        tariff_night = hass_data["tariff_night"]

        # простая модель (без time-of-use)
        cost = float(energy) * tariff_day

        return round(cost, 2)

    @property
    def unit_of_measurement(self):
        return "₽"
