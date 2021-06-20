from serial_watcher import SerialWatcher
from get_ser import serial_ports
import protocol
import constants
import time

sended_move_start_cmd = False
bus_move_start_time = 0
bus_speed = 0
estimated_arrival_time = 0

# (direction, distance)
bus_route_index = 0
bus_route = [(constants.DIR_F, 10), (constants.DIR_F, 10), (constants.DIR_N, 0)]

# def serial_broadcast(serial_objs, data, broadcast):
#     for serial_obj in serial_objs:
#         serial_obj.write(data)

def watch(data, serial, serials, serial_objs):
    sender, command, recv_data = protocol.message_decoding(data)

    if sender == 0 && command == 0 && recv_data == 0:
        print(serial, " : Invalid Protocol")
        return

    if sender == constants.TYPE_BUS:
        if command == constants.CMD_OK && sended_move_start_cmd:
            bus_move_start_time = time.time()
            sended_move_start_cmd = False
            broadcast(protocol.msg_move_direction(bus_route[bus_route_index][0]))
        elif command == constants.CMD_MOVE_END:
            arrival_time = int(time.time() - bus_move_start_time)
            bus_speed = bus_route[bus_route_index][1] // arrival_time
            estimated_arrival_time = int(bus_route[bus_route_index + 1][1] // bus_speed)
            broadcast(protocol.msg_set_arrival_time(estimated_arrival_time))
    elif sender == constants.TYPE_STM32:
        if command == constants.CMD_OK:
            pass
        elif command == constants.CMD_NO:
            broadcast(protocol.msg_set_arrival_time(estimated_arrival_time))
            

def main():
    watcher = SerialWatcher(watch)

    serials = serial_ports()
    for serial in serials:
        watcher.watch(serial)

    watcher.watch_start()
    running = True

    watcher.broadcast(protocol.msg_set_arrival_time(31))

    while running:
        try:
            pass
        except KeyboardInterrupt:
            watcher.watch_stop()
            running = False

if __name__ == '__main__':
    main()