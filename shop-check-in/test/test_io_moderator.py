import Queue

import serial_connection_moderator

class TestSerialConnectionModerator:

    def test_construction(self):
        event_q = Queue.Queue()
        message_q = Queue.Queue()

        serial_connection_moderator.SerialConnectionModerator(event_q, message_q)