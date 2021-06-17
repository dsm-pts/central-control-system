from serial_watcher.watch_serial import WatchSerial
import threading

class SerialWatcher:
    def __init__(self, watch_function):
        self.serials = []
        self.control_datas = {}
        self.data_stacks = {}
        self.serial_objs = {}
        self.watch_function = watch_function

        self.t = None
        self.watching = False

    def watch(self, serial):
        self.serials.append(serial)
        self.control_datas[serial] = { 'stop': False, 'wait': False }
        self.data_stacks[serial] = []
        self.serial_objs[serial] = WatchSerial(
            serial, 
            self.data_stacks[serial], 
            self.control_datas[serial])

    def unwatch(self, serial):
        if serial in serials:
            self.serial_objs[serial].close()
            del self.serial_objs[serial]

            del self.control_datas[serial]
            del self.data_stacks[serial]
        
    def watch_start(self):
        self.t = threading.Thread(target=self.serial_watch_thread)
        self.t.daemon = True
        self.watching = True
        
        self.t.start()

    def watch_stop(self):
        self.watching = False
        self.t.join()
    
    def get_serial(self, serial):
        if serial in self.serial_objs:
            return self.serial_objs[serial].get_serial()
        return None

    def get_watching_serials(self):
        return self.serials

    def send(self, serial, data):
        serial_obj = self.get_serial(serial)
        if serial_obj is not None:
            serial_obj.write(data)

    def serial_watch_thread(self):
        while self.watching:
            for serial in self.serials:
                if len(self.data_stacks[serial]) > 0 and not self.control_datas[serial]['wait']:
                    self.watch_function(self.data_stacks[serial], serial, self.serials, self.serial_objs)

                    while len(self.data_stacks[serial]) > 0:
                        self.data_stacks[serial].pop(0)
        