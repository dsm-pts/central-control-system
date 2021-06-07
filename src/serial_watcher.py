from get_ser import serial_ports
from myserial import MySerial
import threading

class SerialWatcher:
    def __init__(self, watch_function):
        self.serials = serial_ports()
        self.control_datas = {}
        self.data_stacks = {}
        self.serial_objs = {}
        self.watch_function = watch_function

        if len(self.serials) == 0:
            raise Exception('There are no serial ports...')

        for serial in self.serials:
            self.control_datas[serial] = { 'stop': False, 'wait': False }
            self.data_stacks[serial] = []
            self.serial_objs[serial] = MySerial(
                serial, 
                self.data_stacks[serial], 
                self.control_datas[serial])
        
        self.t = None
        self.thread_start()
        
    def thread_start(self):
        self.t = threading.Thread(target=self.serial_watch_thread)
        self.t.daemon = True
        self.t.start()

    def serial_watch_thread(self):
        while True:
            for serial in self.serials:
                if len(self.data_stacks[serial]) > 0 and not self.control_datas[serial]['wait']:
                    self.watch_function(self.data_stacks[serial], serial, self.serials)

                    while len(self.data_stacks[serial]) > 0:
                        self.data_stacks[serial].pop(0)
        