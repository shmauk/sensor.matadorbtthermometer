import asyncio
import logging

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

DEVICE_NAME = "ST10115103"
LOGGER = logging.getLogger(__name__)

async def discover():
    """Discover Bluetooth LE devices."""
    devices = await BleakScanner.discover(timeout=30)
    LOGGER.debug("Discovered devices: %s", [{"address": device.address, "name": device.name} for device in devices])

    named_devices = [device for device in devices if device.name != None]

    return [device for device in named_devices if device.name == "ST10"]

class MatadorInstance:
    def __init__(self, mac: str) -> None:
        self._mac = mac
        self._device = BleakClient(self._mac)
        self._state = None
        self._temperature = None
        self._battery = None

    @property
    def mac(self):
        return self._mac

    @property
    def state(self):
        return self._state

    @property
    def temperature(self):
        return self._temperature

    @property
    def battery(self):
        return self._battery

    async def get_data(self):

        devices_and_adv_data = await BleakScanner.discover(timeout=30,return_adv=True)
        bytes_string = None

        # scanner.discovered_devices_and_advertisement_data[mac][1].manufacturer_data returns a dictionary with 1 entry
        for key in devices_and_adv_data[mac][1].manufacturer_data:
            bytes_string = devices_and_adv_data[mac][1].manufacturer_data[key]

        if bytes_string:
            bytes_array = [x for x in bytes_string]
            thermometer_data = {'mac': self._mac, 'temperature': bytes_array[7], 'battery': bytes_array[9]}
            self._temperature = thermometer_data.get('temperature')
            self._battery = thermometer_data.get('battery')
            self._state = True
        else:
            self._temperature = None
            self._battery = None
            self._state = False