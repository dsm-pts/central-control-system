import serial
import threading

class MySerial:
    def __init__(self, port, data_stack, control_data, baudrate=115200):
        self.__data_stack = data_stack
        self.__control_data = control_data

        self.__serial = serial.Serial(
            port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

        self.t = None
        self.thread_start()

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
        while True:
            if self.__control_data['stop'] == True:
                break
            if len(self.__data_stack) > 0:
                continue

            self.__control_data['wait'] = True

            while self.__serial.read(1) != b'\x02':
                pass
            while True:
                rxdata = self.__serial.read(1)
                if rxdata == b'\x03':
                    break
                self.__data_stack.append(rxdata)
            self.__control_data['wait'] = False

    def send(self, data):
        send_data = b'\x02' + bytes(data, 'ascii') + b'\x03'
        self.__serial.write(send_data)