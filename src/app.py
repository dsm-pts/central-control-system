from serial_watcher import SerialWatcher
from get_ser import serial_ports
import constants

def message_encoding(sender, command, data):
    # Protocol
    # Start(0x02) Sender(1 byte) Command(1 byte) Data_H8(1 byte) Data_L8(1 byte) End(0x03)

    data_h8 = (data & 0xFF00) >> 8
    data_l8 = data & 0x00FF

    sender_byte = sender.to_bytes(1, 'big')
    command_byte = command.to_bytes(1, 'big')
    data_h8_byte = data_h8.to_bytes(1, 'big')
    data_l8_byte = data_l8.to_bytes(1, 'big')

    return b'\x02' + sender_byte + command_byte + data_h8_byte + data_l8_byte + b'\x03'

def message_decoding(msg):
    if len(msg) < 5:
        print('invalid protocol')
    sender = msg[1]
    command = msg[2]

    data_h8 = msg[3]
    data_l8 = msg[4]

    data = (data_h8 << 8) | data_l8

    return (sender, command, data)

def watch(data, serial, serials, serial_objs):
    print(serial, ': rx', data)

def main():
    watcher = SerialWatcher(watch)

    serials = serial_ports()
    for serial in serials:
        watcher.watch(serial)

    watcher.watch_start()
    running = True

    watcher.broadcast(message_encoding(constants.TYPE_RPI, constants.CMD_SET_SECONDS, 31))

    while running:
        try:
            pass
        except KeyboardInterrupt:
            watcher.watch_stop()
            running = False

if __name__ == '__main__':
    main()