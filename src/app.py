from serial_watcher import SerialWatcher
from get_ser import serial_ports

def watch(data, serial, serials, serial_objs):
    print('rx', data)

def main():
    watcher = SerialWatcher(watch)

    serials = serial_ports()
    for serial in serials:
        watcher.watch(serial)

    watcher.watch_start()
    running = True
    
    watcher.send(serials[0], bytes('\x02\x01\x01\x00\x1f\x03', 'ascii'))

    while running:
        try:
            pass
        except KeyboardInterrupt:
            watcher.watch_stop()
            running = False

if __name__ == '__main__':
    main()