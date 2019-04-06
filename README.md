# Description

Homeassistant component for connecting to an openwebnet gateway.

Usage:

- Install homeassistant
- Install https://github.com/karel1980/openwebnet
- Copy the files in this repository to `<PATH_TO_HASS_CONFIG>/customer_components/my_home`. Symlinks also work.
- Add example configuration to `<PATH_TO_HASS_CONFIG>/configuration.yml`

# Example configuration

```yaml
my_home:
  host: '192.168.1.5'
  port: 20000
  password: '123456'

light:
  - platform: my_home
    scan_interval: 5
    devices:
      - name: kitchen_light
        address: '13'
      - name: bedroom_light
        address: '10'
