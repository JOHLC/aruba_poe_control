"""Aruba PoE Control integration."""
import logging

_LOGGER = logging.getLogger(__name__)

# The integration will be automatically set up by the config flow
async def async_setup(hass, config):
    """Set up the Aruba PoE Control integration."""
    _LOGGER.info("Aruba PoE Control integration is set up.")
    return True
