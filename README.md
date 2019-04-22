# Description

Homeassistant component for connecting to an openwebnet gateway.
Communication with the gateway happens via the reopenwebnet client.

Usage:

- Install homeassistant
- Copy the files in this repository to `<PATH_TO_HASS_CONFIG>/customer_components/hass_reopenwebnet`.
- Add example configuration to `<PATH_TO_HASS_CONFIG>/configuration.yml`

# Example configuration

```yaml
reopenwebnet:
  host: '192.168.1.5'
  port: 20000
  password: '123456'

light:
  - platform: reopenwebnet
    scan_interval: 5
    devices:
      - name: kitchen_light
        address: '13'
      - name: bedroom_light
        address: '10'
