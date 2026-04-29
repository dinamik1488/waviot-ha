import voluptuous as vol
from homeassistant import config_entries

class WaviotConfigFlow(config_entries.ConfigFlow, domain="waviot"):

    async def async_step_user(self, user_input=None):

        if user_input:
            return self.async_create_entry(
                title=user_input["modem_id"],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("modem_id"): str,
                vol.Required("api_key"): str,
                vol.Required("tariff_day"): float,
                vol.Required("tariff_night"): float,
            }),
        )
