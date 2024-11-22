import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

class ArubaPoEControlConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for Aruba PoE Control."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user input for the initial configuration."""
        if user_input is None:
            # Show a form where the user inputs their Aruba switch settings
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_HOST): str,
                        vol.Required(CONF_USERNAME): str,
                        vol.Required(CONF_PASSWORD): str,
                        vol.Required("port"): int,
                    }
                ),
            )

        # Validate the user input and test the connection
        host = user_input[CONF_HOST]
        username = user_input[CONF_USERNAME]
        password = user_input[CONF_PASSWORD]
        port = user_input["port"]

        # Test the connection to the Aruba switch
        if await self._test_connection(host, username, password, port):
            # Successfully validated the input, create the entry
            return self.async_create_entry(
                title=f"Aruba PoE Control - {host}",
                data=user_input,
            )
        else:
            # If connection fails, show an error message and prompt for re-entry
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_HOST): str,
                        vol.Required(CONF_USERNAME): str,
                        vol.Required(CONF_PASSWORD): str,
                        vol.Required("port"): int,
                    }
                ),
                errors={"base": "cannot_connect"},
            )

    async def _test_connection(self, host, username, password, port):
        """Test if we can successfully connect to the Aruba switch."""
        import requests

        try:
            # Send a simple request to check if the connection is valid
            url = f"https://{host}/rest/v10.04/system/ports/{port}/power"
            headers = {"Content-Type": "application/json"}
            data = {"enable": False}  # Sample request to test connection

            response = requests.put(
                url,
                json=data,
                auth=(username, password),
                headers=headers,
                verify=False,
            )

            # If the response status code is 200, it's a successful connection
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            _LOGGER.error(f"Error connecting to Aruba switch: {e}")
            return False
