import threading
import Queue

import serial

import event

COM_PORT = 'COM3'
import logger.all_events as event_logger

BAUD_RATE = 115200
TIMEOUT_SECONDS = 0.05

EVENT_KEY_START_INDEX = 0
EVENT_KEY_END_INDEX = 2
EVENT_DATA_START_INDEX = EVENT_KEY_END_INDEX


class IoModerator(threading.Thread):

    def __init__(self, event_q, message_q):
        super(IoModerator, self).__init__()

        self._event_q = event_q
        self._message_q = message_q

    def run(self):
        with serial.Serial(COM_PORT, BAUD_RATE, timeout=TIMEOUT_SECONDS) as serial_port:
            while True:
                try:
                    message = self._message_q.get(timeout=TIMEOUT_SECONDS)
                except Queue.Empty:
                    continue
                else:
                    event_logger.log_display_message(message)
                    serial_port.write(message)
                finally:
                    self._enqueue_events(serial_port)

    def _enqueue_events(self, serial_port):
        while serial_port.inWaiting():
            message = serial_port.readline()
            new_event = self._convert_message_to_event(message)
            event_logger.log_event_enqueue(new_event)
            self._event_q.put(new_event)

    def _convert_message_to_event(self, message):
        event_key = message[EVENT_KEY_START_INDEX:EVENT_KEY_END_INDEX]
        event_data = message[EVENT_DATA_START_INDEX:]  # Empty list if index is out of bounds.
        if event_key == event.CARD_INSERT or event_key == event.CARD_REMOVE:
            event_data = int(event_data)
        return event.Event(event_key, event_data)


def safe_format_msg(msg):
    # Split into lines
    lines = msg.split('\n\r')
    # Make sure first line has null byte
    if lines[0][0:1] != '\0':
        lines[0] = '\0' + lines[0]
    # Truncate Lines
    lines = [line[:16] for line in lines]
    # Re combine
    safe_msg = '\n\r'.join(lines)
    if safe_msg != msg:
        print "Bad format, msg: %s" % msg
    return safe_msg


def main():
    event_q = Queue.Queue()
    message_q = Queue.Queue()
    message_q.put("\0TESTING")
    IoModerator(event_q, message_q).run()


if __name__ == "__main__":
    main()
