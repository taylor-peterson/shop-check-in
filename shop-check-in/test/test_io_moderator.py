import Queue

import io_moderator


class TestIoModerator(object):

    def test_construction(self):
        event_q = Queue.Queue()
        message_q = Queue.Queue()

        io_moderator.IoModerator(event_q, message_q)