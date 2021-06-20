from serial_watcher import SerialWatcher
from get_ser import serial_ports
import constants

def watch(data, serial, serials, serial_objs):
    print(serial, ': rx', data)

def make_msg_with_protocol(type, command, data):
    # Protocol
    # Start(0x02) Type(1 byte) Command(1 byte) Data_H8(1 byte) Data_L8(1 byte) End(0x03)

    data_h8 = (data & 0xFF00) >> 8
    data_l8 = data & 0x00FF

    type_byte = type.to_bytes(1, 'big')
    command_byte = command.to_bytes(1, 'big')
    data_h8_byte = data_h8.to_bytes(1, 'big')
    data_l8_byte = data_l8.to_bytes(1, 'big')

    return b'\x02' + type_byte + command_byte + data_h8_byte + data_l8_byte + b'\x03'



def main():
    watcher = SerialWatcher(watch)

    serials = serial_ports()
    for serial in serials:
        watcher.watch(serial)

    watcher.watch_start()
    running = True

    watcher.broadcast(make_msg_with_protocol(constants.TYPE_RPI, constants.CMD_SET_SECONDS, 31))

    while running:
        try:
            pass
        except KeyboardInterrupt:
            watcher.watch_stop()
            running = False

if __name__ == '__main__':
    main()