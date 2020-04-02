import serial
from serial.tools import list_ports

if __name__ == '__main__':
    for LPI in serial.tools.list_ports.grep(""):
        print()
        print('device: %s' % LPI.device)
        print('name: %s' % LPI.name)
        print('description: %s' % LPI.description)
        print('hwid: %s' % LPI.hwid)
        print('vid: %s' % LPI.vid)
        print('pid: %s' % LPI.pid)
        print('serial_number: %s' % LPI.serial_number)
        print('location: %s' % LPI.location)
        print('manufacturer: %s' % LPI.manufacturer)
        print('product: %s' % LPI.product)
        print('interface: %s' % LPI.interface)

