# Home Assistant Aruba PoE Control Integration

This custom Home Assistant integration allows you to control and monitor Power over Ethernet (PoE) ports on an Aruba 2530 series switch. With this integration, you can:

- Enable or disable PoE on specific ports.
- Monitor PoE power consumption.
- Check port status (up or down).

## Features

- **Control PoE**: Turn PoE on or off for specific ports.
- **Port Status**: Get the status (up/down) of each port.

## Requirements

- Home Assistant instance (version 2021.3 or newer recommended).
- Aruba 2530 series switch with REST API enabled.
- The switch must be accessible via HTTPS (with the appropriate credentials).
