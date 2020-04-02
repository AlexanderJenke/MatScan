import usb.core

VENDOR_ID = 0x0bf8
PRODUCT_ID = 0x104031815411022
4031815411022
0c

if __name__ == '__main__':

    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        raise ValueError('Our device is not connected')

    print(dev)

    print("Setting configuration")
    dev.set_configuration()
    print("Configuration set")

    cfg = dev.get_active_configuration()

    print("Active configuration")
    print(cfg)

    print("intf")
    intf = cfg[(0, 0)]
    print(intf)
