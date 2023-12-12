#bootloader_comm.py
import can
CAN_NO_ANSWER             = 0x00
CAN_NACK                  = 0x1F
CAN_ACK                   = 0x79
GET_COMMAND               = 0x00
GET_VER_RP_STATUS_COMMAND = 0x01
GET_ID_COMMAND            = 0x02
SPEED_COMMAND             = 0x03
READ_MEM_COMMAND          = 0x11
GO_COMMAND                = 0x21
WRITE_MEM_COMMAND         = 0x31
ERASE_COMMAND             = 0x43
WRITE_PROTECT_COMMAND     = 0x63
WRITE_UNPROTECT_COMMAND   = 0x73
READOUT_PROTECT_COMMAND   = 0x82
READOUT_UNPROTECT_COMMAND = 0x92


def start_bootloader():
    print("Start bootloader: ")    
    start_can_message = (CAN_ACK,0,0x00)    
    can_bus=config_can_bus()
    send_can_message(can_bus, start_can_message)
    device_answer=get_chip_answer(CAN_ACK,can_bus)
    can_bus.shutdown()    
    if device_answer == CAN_NO_ANSWER:
        print("sBoot No Answer\n")        
        return False
    elif device_answer == CAN_ACK:
        print("sBoot ACK\n")
        return True
    elif device_answer == CAN_NACK:
        print("sBoot NACK\n")
        return True 
    else:     
        print("sBoot Error\n")        
        return False

def chip_ID_response():
    get_id_command = (GET_ID_COMMAND,0,0x00)
    print("Configuring chipID ")
    can_bus=config_can_bus()
    send_can_message(can_bus, get_id_command)
    device_answer=get_chip_answer(GET_ID_COMMAND,can_bus) #0x002#0x79
    print(f"device answer: {device_answer}")
    if device_answer == CAN_ACK:
        print("Waiting Chip ID response ")
        try:
            receivedmessage = can_bus.recv(timeout=5.0)
        except can.canError as e:
            print(f"error of can{e}")
            
        else :
            try:
                addressZero = receivedmessage.data[0]
                addressOne = receivedmessage.data[1] 
                print(f"Chip ID: {addressZero},{addressOne}")
                #print(f"Integer ID_value:{ord(addressZero)},{ord(addressOne)}")
            except AttributeError as tye:
                print(f"error of type error:{tye}")                 
    elif device_answer == CAN_NACK:
        print("Chip ID: NACK")
    else:     
        print("Chip ID: No Answer")
    can_bus.shutdown()
    
def config_can_bus():
    bus=can.Bus(interface='socketcan',
                channel='can0',
                receive_own_messages=False,
                bitrate=500000)    
    return bus

def send_can_message(can_bus, can_message):
    message = can.Message(arbitration_id=can_message[0], 
                          data=can_message[2],
                          dlc=can_message[1],
                          is_extended_id=True                         
                          )
    can_bus.send(message, timeout=0.2)    

def get_chip_answer(can_ID, can_bus):       
    try:        
     receivedmessage = can_bus.recv(timeout=4.0)     
    except can.canError as e:
        print(f"error of can{e}")
        return CAN_NO_ANSWER
    else :        
        try:
            print(f"Response received:{receivedmessage.arbitration_id},{receivedmessage.data}")
            if receivedmessage.arbitration_id == can_ID:            
                if int.from_bytes(receivedmessage.data) == CAN_ACK:                    
                    return CAN_ACK
                elif int.from_bytes(receivedmessage.data) == CAN_NACK:                    
                    return CAN_NACK
                else:                    
                    return CAN_NO_ANSWER         
            else:                
                return CAN_NO_ANSWER
        except AttributeError as tye:
            print(f"error of type error:{tye}") 
            return CAN_NO_ANSWER
    finally:
        print(f"end of get_chip_answer: {can_ID}")

