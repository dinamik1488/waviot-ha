async def async_setup_entry(hass, entry):
    hass.data.setdefault("waviot", {})
    return True
