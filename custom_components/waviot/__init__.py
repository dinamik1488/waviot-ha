async def async_setup_entry(hass, entry):
    coordinator = WaviotCoordinator(
        hass,
        entry.data["modem_id"],
        entry.data["api_key"]
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("waviot", {})
    hass.data["waviot"][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True
