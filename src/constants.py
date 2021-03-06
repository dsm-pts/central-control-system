# Sender Types
TYPE_RPI = 0x01
TYPE_STM32 = 0x02
TYPE_BUS = 0x13

# Commands - ACK
CMD_OK = 0x01
CMD_NO = 0x02

# Commands - GLCD
CMD_SET_SECONDS = 0x13

# Commands - RF
CMD_RECV_RF = 0x04
CMD_SEND_RF = 0x05

# Commands - BUS
CMD_MOVE_START = 0x06
CMD_MOVE_END = 0x07
CMD_MOVE = 0x08

# Directions
DIR_F = 0x01 # 0000 0001
DIR_B = 0x02 # 0000 0010
DIR_R = 0x04 # 0000 0100
DIR_L = 0x08 # 0000 1000
DIR_N = 0x10 # 0001 0000