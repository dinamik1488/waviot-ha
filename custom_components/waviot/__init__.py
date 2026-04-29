from .coordinator import WaviotCoordinator

async def async_setup_entry(hass, entry):

    coordinator = WaviotCoordinator(
        hass,
        entry.data["modem_id"],
        entry.data["api_key"]
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("waviot", {})
    hass.data["waviot"][entry.entry_id] = {
        "coordinator": coordinator,
        "tariff_day": entry.data["tariff_day"],
        "tariff_night": entry.data["tariff_night"],
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass, entry):

    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])

    if unload_ok:
        hass.data["waviot"].pop(entry.entry_id)

    return unload_ok
