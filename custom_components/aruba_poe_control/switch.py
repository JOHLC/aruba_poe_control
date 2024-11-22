import logging
import requests
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

# Define the Switch class for controlling the PoE on the Aruba switch
class ArubaPoESwitch(SwitchEntity):
    """Representation of an Aruba PoE-controlled switch port."""

    def __init__(self, host, username, password, port):
        """Initialize the switch."""
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self._is_on = False

    def _send_request(self, enable_poe):
        """Send a request to the Aruba switch to enable or disable PoE."""
        url = f"https://{self.host}/rest/v10.04/system/ports/{self.port}/power"
        headers = {
            "Content-Type": "application/json",
        }
        data = {"enable": enable_poe}
        try:
            response = requests.put(
                url,
                json=data,
                auth=(self.username, self.password),
                headers=headers,
                verify=False,
            )
            if response.status_code == 200:
                _LOGGER.info(f"Successfully updated PoE on port {self.port}")
                return True
            else:
                _LOGGER.error(f"Failed to update PoE on port {self.port}: {response.text}")
                return False
        except Exception as e:
            _LOGGER.error(f"Error communicating with Aruba switch: {e}")
            return False

    @property
    def name(self):
        """Return the name of the switch."""
        return f"Aruba PoE Port {self.port}"

    @property
    def is_on(self):
        """Return the state of the switch (PoE enabled or disabled)."""
        return self._is_on

    def turn_on(self):
        """Turn on PoE for this port."""
        if self._send_request(True):
            self._is_on = True
            self.schedule_update_ha_state()

    def turn_off(self):
        """Turn off PoE for this port."""
        if self._send_request(False):
            self._is_on = False
            self.schedule_update_ha_state()

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Aruba PoE switch."""
    host = config[CONF_HOST]
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    port = config["port"]

    switch = ArubaPoESwitch(host, username, password, port)
    async_add_entities([switch], True)
