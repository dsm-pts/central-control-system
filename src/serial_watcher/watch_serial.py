import serial
import threading

class WatchSerial:
    def __init__(self, port, data_stack, control_data, baudrate=115200):
        self.__data_stack = data_stack
        self.__control_data = control_data
        self.serial_port = port
        self.__serial = serial.Serial(
            port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

        self.t = None
        self.thread_start()

    def get_serial(self):
        return self.__serial

    def close(self):
        self.thread_stop()
        self.get_serial().close()

    def thread_start(self):
        self.t = threading.Thread(target=self.read_data_thread)
        self.t.daemon = True
        self.t.start()

    def thread_stop(self):
        if self.__control_data['stop'] == True:
            return
        self.__control_data['stop'] = True
        self.t.join()

    def read_data_thread(self):
        while not self.__control_data['stop']:
            if len(self.__data_stack) > 0:
                continue

            self.__control_data['wait'] = True

            rx_data = 0
            while rx_data != b'\x02':
                rx_data = self.__serial.read(1)

            self.__data_stack.append(b'\x02')
            
            while True:
                rxdata = self.__serial.read(1)
                if rxdata == b'\x03':
                    self.__data_stack.append(b'\x03')
                    break
                self.__data_stack.append(rxdata)
            self.__control_data['wait'] = False