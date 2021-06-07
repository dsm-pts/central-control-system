from serial_watcher.serial_watcher import SerialWatcher

def watch(data, serial, serials, serial_objs):
    # for other_serial in serials:
    #     if other_serial != serial:
    #         print('tx', data)
    #         other_serial.send(data)
    print('rx', data)

def main():
    watcher = SerialWatcher(watch)
    watcher.broadcast('\x01\x01\x00\x1f')

    running = True
    while running:
        try:
            pass
        except KeyboardInterrupt:
            running = False

if __name__ == '__main__':
    main()