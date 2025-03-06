import argparse
import asyncio
import struct
import pyautogui

from bleak import BleakClient, BleakScanner

'''
Script to discover and read out the measurements.

    arguments: --client "XX:XX:XX:XX:XX"
      directly connects to the client device.
      if no argument is given, the first device with "Disto" in its name is selected.

TODO: disconnect gracefully

'''

# UUIDs
#DISTO_SERVICE_UUID = "3AB10100-F831-4395-B29D-570977D5BF94"
DISTO_DISTANCE_UUID = "3AB10101-F831-4395-B29D-570977D5BF94"
#DISTO_COMMAND_UUID = "3AB10109-F831-4395-B29D-570977D5BF94"

# Function to find the DISTO D1 device
async def find_disto():
    devices = await BleakScanner.discover()
    for device in devices:
        if "DISTO" in (device.name or ""):  # Adjust if needed
            print(f"Found Leica DISTO D1: {device.name} - {device.address}")
            return device.address
    print("Leica DISTO D1 not found.")
    return None

# Callback function for receiving distance data
def distance_callback(sender, data):

    if len(data) >= 4:
        distance = struct.unpack('<f', data)[0] # little endian float
        print(f'Distance: ', distance)

        KEYBOARD_WRITE = True
        if KEYBOARD_WRITE:
            pyautogui.write(f'{distance*1000:.0f}')  # Types "4244" for 4.244m
            pyautogui.press('enter')

# Function to connect and read distance
async def read_distance(device_address):
    async with BleakClient(device_address) as client:
        print(f"Connected to {device_address}")

        # Enable notifications for distance data
        await client.start_notify(DISTO_DISTANCE_UUID, distance_callback)

        # Wait for distance data (30 minutes)
        await asyncio.sleep(1800)

        # Stop notifications
        await client.stop_notify(DISTO_DISTANCE_UUID)


async def main(device_address):
    if device_address is None:
        device_address = await find_disto()    

    if device_address:
        await read_distance(device_address)


if __name__ == '__main__':
    # Command Line Arguments
    parser = argparse.ArgumentParser(description='Process input and output PDF files.')
    parser.add_argument('--client', type=str, default=None, help='Client MAC to connect')    
    args = parser.parse_args()
    
    # Run Async
    asyncio.run(main(args.client))