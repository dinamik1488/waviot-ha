from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import SENSORS

SENSOR_KEYS = list(SENSORS.keys())

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["waviot"][entry.entry_id]

    entities = []
    for key in SENSOR_KEYS:
        entities.append(WaviotSensor(coordinator, key))

    async_add_entities(entities)


class WaviotSensor(CoordinatorEntity, Entity):
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
        try:
            if self.key in self.coordinator.data["modem"]:
                return self.coordinator.data["modem"][self.key]

            return self.coordinator.data["values"].get(self.key, {}).get("last_value")
        except:
            return None

    @property
    def unit_of_measurement(self):
        return SENSORS[self.key]["unit"]
