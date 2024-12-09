from bluepy import btle
import struct
import time
import sys

class SensorTag(btle.Peripheral):
    def __init__(self, addr):
        btle.Peripheral.__init__(self, addr)

    def enable_temperature(self, sensor_id):
        # Temperature service and characteristic UUIDs are the same for both sensors
        service_uuid = btle.UUID("f000aa00-0451-4000-b000-000000000000")
        data_uuid = btle.UUID("f000aa01-0451-4000-b000-000000000000")
        config_uuid = btle.UUID("f000aa02-0451-4000-b000-000000000000")

        serv = self.getServiceByUUID(service_uuid)
        conf_char = serv.getCharacteristics(config_uuid)[0]
        data_char = serv.getCharacteristics(data_uuid)[0]

        # Enable the temperature sensor
        conf_char.write(b"\x01")
        return data_char

    def read_temperature(self, char):
        raw_data = char.read()
        raw_val = struct.unpack('<h', raw_data[:2])[0]
        temp = raw_val / 128.0
        return temp

    def enable_humidity(self, sensor_id):
        # Humidity service and characteristic UUIDs are the same for both sensors
        service_uuid = btle.UUID("f000aa20-0451-4000-b000-000000000000")
        data_uuid = btle.UUID("f000aa21-0451-4000-b000-000000000000")
        config_uuid = btle.UUID("f000aa22-0451-4000-b000-000000000000")

        serv = self.getServiceByUUID(service_uuid)
        conf_char = serv.getCharacteristics(config_uuid)[0]
        data_char = serv.getCharacteristics(data_uuid)[0]

        # Enable the humidity sensor
        conf_char.write(b"\x01")
        return data_char

    def read_humidity(self, char):
        raw_data = char.read()
        raw_hum = struct.unpack('<H', raw_data[2:4])[0]
        hum = raw_hum / 65536.0 * 100.0
        return hum

# Replace with your sensors' MAC addresses
mac_address_sensor = "PUT_MAC_ADDRESS"  # AAL house

try:
    sensortag = SensorTag(mac_address_sensor)

    # Enable sensor for SensorTag
    temp_char = sensortag.enable_temperature(1)
    hum_char = sensortag.enable_humidity(1)

    while True:
        # Read and display data from sensor
        temperature = sensortag.read_temperature(temp_char)
        humidity = sensortag.read_humidity(hum_char)

        # Structured output
        sys.stdout.write(f"{temperature:.2f} C | {humidity:.2f} % \n")
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("\nInterrupted by user")
finally:
    # Ensure disconnection from both sensors
    sensortag.disconnect()
