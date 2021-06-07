from serial_watcher import SerialWatcher

def watch(data, serial, serials):
    for other_serial in serials:
        if other_serial != serial:
            print('tx', data)
            other_serial.send(data)
    print('rx', data)

def main():
    watcher = SerialWatcher(watch)

    running = True
    while running:
        try:
            pass
        except KeyboardInterrupt:
            running = False

if __name__ == '__main__':
    main()