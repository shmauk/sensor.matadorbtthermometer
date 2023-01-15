# sensor.matadorbtthermometer

This is an integration for the Matador Intelligent Bluetooth Food Thermometer for home-assistant.

It will need to be manually added through the config.yaml file using the following and the MAC of your thermometer:

```
sensor:
  - platform: matador
    name: "Matador Thermometer"
    mac: "XX:XX:XX:XX:XX:XX"
```

Currently this does not use the new bluetooth integration from home-assistant but will be updated to do so that in the future.
