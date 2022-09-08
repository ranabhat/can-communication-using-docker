import can
import time

class _CanData:
    def __init__(self,
                 message=[],
                 error=None,
                 is_station_ok=None,
                 channel='can0',
                 bustype='socketcan',
                 bus_is_available=None,
                 bus=None,
                 ):
        self.message = message
        self.error = error
        self.is_station_ok = is_station_ok
        self.channel = channel
        self.bustype = bustype
        self.bus_is_available = bus_is_available
        self.bus = bus
    
    def check_if_can_bus_is_avaiable(self):
        try:
            self.bus = can.interface.Bus(channel=self.channel, bustype=self.bustype)
        except OSError:
            self.bus_is_available = False
            raise
        except can.CanError:
            self.bus_is_available = False
            raise AttributeError("Can Internal Issues originally") 
        except AttributeError:
            self.bus_is_available = False
            raise
        else:
            self.bus_is_available = True

    @staticmethod
    def change_to_hex(data):
        return data.hex()

    @staticmethod
    def change_hex_data_to_generator_list_expression(data):
        """
        Arguments
        hex_data: '4002240200000000' 
        Returns <generator object <genexpr> at 0x75afab18>

        when list(gen), change to  ['40', '02', '24', '02', '00', '00', '00', '00']
        """

        # <generator object <genexpr> at 0x75afab18>
        return (data[i:i + 2] for i in range(0, len(data), 2))

    @staticmethod
    def change_to_complete_message_in_list_form(arbitration_id, dlc,
                                                generator_data):
        """
        Arguments
        arbitration_id: 534 (in hex 0x216)
        dlc: 8
        generator_data: <generator object <genexpr> at 0x75afab18>

        Returns ['216', '08','00', '00', '00', '00', '3d', '00', '60', '01']
        """
        message = (((hex(arbitration_id)).lstrip('0x') + ' ' +
                    str(dlc).zfill(2)).rsplit()) + list(generator_data)
        return message

    def from_canbus_transform_message(self):
        try:
        #     bus = self.get_can_bus()
        # except AttributeError:
        #     raise
        # except OSError:
        #     raise
        # else:
            message = self.bus.recv()  # Wait until message is received
            # (message.data).hex() -->'4002240200000000'
            data = _CanData.change_to_hex(message.data)
            # (data[i:i+2] for i in range(0, len(data), 2)) #<generator object <genexpr> at 0x75afab18>
            gen_data = _CanData.change_hex_data_to_generator_list_expression(
                data)
            v13 = _CanData.change_to_complete_message_in_list_form(
                message.arbitration_id, message.dlc, gen_data)
            return v13
        except can.CanError:
            self.bus_is_available = False
            raise AttributeError("Can Internal Issues originally")
        except AttributeError:
            self.bus_is_available = False
            raise
        except OSError:
            self.bus_is_available = False
            raise

    def create_can_message(self, id, **bits):
        """Create a can message to be sent to can bus
        ---> can.Message(arbitration_id=115,data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00,0x00],extended_id=False)

        Arguments:
        id: arbitration id of the message (0x115 | 0x215 | or any other)
        Keyword arguments:
            first_bit=  0x00 | 0x01 | other 
            second_bit= 0x00 | 0x01 | other 
            third_bit=  0x00 | 0x01 | other 
            fourth_bit= 0x00 | 0x01 | other 
            fifth_bit=  0x00 | 0x01 | other 
            sixth_bit=  0x00 | 0x01 | other 
            seventh_bit=0x00 | 0x01 | other 
            eigth_bit=  0x00 | 0x01 | other

        Returns can message: Timestamp:        0.000000        ID: 0115    S                DLC:  8    00 00 00 00 01 00 00 00
        """

        bit_dict = {
            'first_bit': 0x00,
            'second_bit': 0x00,
            'third_bit': 0x00,
            'fourth_bit': 0x00,
            'fifth_bit': 0x00,
            'sixth_bit': 0x00,
            'seventh_bit': 0x00,
            'eighth_bit': 0x00
        }
        for bit in bits.keys():
            bit_dict[bit] = bits[bit]
        self.msg = can.Message(arbitration_id=id,
                               data=bit_dict.values(),
                               is_extended_id=False)
        return self.msg

    def send_can_message(self, message):
        try:
        #     bus = self.get_can_bus()
        # except AttributeError:
        #     raise
        # except OSError:
        #     raise
        # else:
            self.bus.send(message)
        except can.CanError:
            self.bus_is_available = False
            raise AttributeError("Can Internal Issues originally")
        except AttributeError:
            self.bus_is_available = False
            raise
        except OSError:
            self.bus_is_available = False
            raise
    
    def send_heart_beat(self):
        message = self.create_can_message(0xFF, first_bit=0x01)
        self.send_can_message(message)

_instance = None

#### Naive singleton implementation
def CanData():
    global _instance
    if _instance is None:
        _instance = _CanData()
        _instance.check_if_can_bus_is_avaiable()
    return _instance

can_read = CanData()
while True:
    start_msg = can_read.create_can_message(0x115, first_bit=0x01)
    print(f"start messgae {start_msg}")
    can_read.send_can_message(start_msg)
    print(f"Connector 2 Started")
    stop_msg = can_read.create_can_message(0x115, first_bit=0x00)
    time.sleep(10)
    print(f"stop messgae {stop_msg}")
    can_read.send_can_message(stop_msg)
    break
