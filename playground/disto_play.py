
import asyncio
from bleak import BleakScanner, BleakClient

'''
    Connect with the disto d1 laser
'''

# Get devices
async def scan_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f'Device: {device}, address: {device.address}')

#asyncio.run(scan_devices())
# Address is FD:33:8C:36:69:E5

DEVICE_ADDRESS = "FD:33:8C:36:69:E5"
CHARACTERISTIC_UUID = "3ab1010a-f831-4395-b29d-570977d5bf94"


'''
Service: 00001801-0000-1000-8000-00805f9b34fb - 00001801-0000-1000-8000-00805f9b34fb (Handle: 8): Generic Attribute Profile
  Characteristic: 00002a05-0000-1000-8000-00805f9b34fb - 00002a05-0000-1000-8000-00805f9b34fb (Handle: 9): Service Changed
Service: 0000180a-0000-1000-8000-00805f9b34fb - 0000180a-0000-1000-8000-00805f9b34fb (Handle: 31): Device Information
  Characteristic: 00002a29-0000-1000-8000-00805f9b34fb - 00002a29-0000-1000-8000-00805f9b34fb (Handle: 32): Manufacturer Name String
Service: 3ab10100-f831-4395-b29d-570977d5bf94 - 3ab10100-f831-4395-b29d-570977d5bf94 (Handle: 12): Unknown
  Characteristic: 3ab10102-f831-4395-b29d-570977d5bf94 - 3ab10102-f831-4395-b29d-570977d5bf94 (Handle: 16): Unknown
  Characteristic: 3ab1010c-f831-4395-b29d-570977d5bf94 - 3ab1010c-f831-4395-b29d-570977d5bf94 (Handle: 24): Unknown
  Characteristic: 3ab10101-f831-4395-b29d-570977d5bf94 - 3ab10101-f831-4395-b29d-570977d5bf94 (Handle: 13): Unknown
  Characteristic: 3ab10109-f831-4395-b29d-570977d5bf94 - 3ab10109-f831-4395-b29d-570977d5bf94 (Handle: 19): Unknown
  Characteristic: 3ab1010a-f831-4395-b29d-570977d5bf94 - 3ab1010a-f831-4395-b29d-570977d5bf94 (Handle: 21): Unknown
Service: 0000180f-0000-1000-8000-00805f9b34fb - 0000180f-0000-1000-8000-00805f9b34fb (Handle: 26): Battery Service
  Characteristic: 00002a19-0000-1000-8000-00805f9b34fb - 00002a19-0000-1000-8000-00805f9b34fb (Handle: 27): Battery Level
  Characteristic: 00002a1a-0000-1000-8000-00805f9b34fb - 00002a1a-0000-1000-8000-00805f9b34fb (Handle: 29): Battery Power State

  from github:
  private let distoCharateristicDistance = "3AB10101-F831-4395-B29D-570977D5BF94"
  private let distoCharateristicCommand = "3AB10109-F831-4395-B29D-570977D5BF94"

  #start scanning: 3ab10100-f831-4395-b29d-570977d5bf94 service
'''

# Scan for Services:
async def get_services():
    async with BleakClient(DEVICE_ADDRESS) as client:
        for service in client.services:
            print(f"Service: {service.uuid} - {service}")

            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} - {char}")

#asyncio.run(get_services())

async def read_data():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print(f"Connected: {client.is_connected}")

        # Read characteristic value
        data = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print(f"Received Data: {data}")

#asyncio.run(read_data())

def callback(sender, data):
    print(f"Received from {sender}: {data}")

async def listen():
    async with BleakClient(DEVICE_ADDRESS) as client:
        await client.start_notify(CHARACTERISTIC_UUID, callback)
        await asyncio.sleep(30)  # Listen for 30 seconds
        await client.stop_notify(CHARACTERISTIC_UUID)

asyncio.run(listen())
