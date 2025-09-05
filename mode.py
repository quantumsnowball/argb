from openrgb import OpenRGBClient
from openrgb.utils import DeviceType, ModeData

client = OpenRGBClient(port=6742)
client.clear()  # Turns everything off
device = client.get_devices_by_type(DeviceType.MOTHERBOARD)[0]
device.set_mode('Color shift', save=True)
device.modes[device.active_mode].speed = 255
