import event
import serial

COM_PORT = 'COM8'
BAUD_RATE = 115200


event_key = {
    "M1":event.CARD_INSERT,
    "M0":event.CARD_REMOVE,
    "S1":event.SWITCH_FLIP_ON,
    "S0":event.SWITCH_FLIP_OFF,
    "B1": (
        event.BUTTON_CANCEL,
        event.BUTTON_CONFIRM,
        event.BUTTON_MONEY,
        event.BUTTON_CHANGE_POD,
        event.BUTTON_DISCHARGE_USER,
        )
    }
    



class Teensy():

    def __init__(self, event_q):
        self._event_q = event_q
        ser = serial.Serial(COM_PORT, BAUD_RATE)
        ser.close()
        # TODO: Error handling if unable to open serial port

    def open_serial(self):
        ser.open()

    def close_serial(self):
        ser.close()

    def print_lcd(self, string):
        ser.open()
        ser.write(string)
        ser.close()

    def scan(self):
        if (ser.inWaiting() > 0):
            update = ser.readline()
        
        '''teensy_event = event.Event(event_key[]......'''
        self._event_q.put(teensy_event)






