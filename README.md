# Description

Homeassistant component for connecting to an openwebnet gateway.

Usage:

- Install homeassistant
- Copy this repository to `<PATH_TO_HASS_CONFIG>/customer_components/my_home`
- Add example configuration to `<PATH_TO_HASS_CONFIG>/configuration.yml`

# Example configuration

```yaml
my_home:
  host: '192.168.1.10'
  port: 20000
  password: '951753'

light:
  - platform: my_home
    scan_interval: 5
    devices:
      - name: test_light
        address: '13'
      - name: eettafel
        address: '10'
      - name: wand_voor
        address: '11'
```
