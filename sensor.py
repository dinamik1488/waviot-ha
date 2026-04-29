from homeassistant.helpers.entity import Entity

class WaviotSensor(Entity):
    def __init__(self, coordinator, rid):
        self.coordinator = coordinator
        self.rid = rid

    @property
    def name(self):
        return f"waviot_{self.rid}"

    @property
    def state(self):
        try:
            return self.coordinator.data["data"]["registrators"][self.rid]["last_value"]
        except:
            return None
