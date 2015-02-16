import re  # Regular expressions
import threading
import Queue as queue
import collections

import pyHook  # Callbacks for keyboard events
import pythoncom  # Tie in to Windows events

import event

import logger.all_events as event_logger

ID_READ_LENGTH = 12
ID_REGEX = ";[0-9]{10}\x00"


class IdLogger(threading.Thread):
    """ Listens to keyboard input and reports any properly formatted
        IDs that it finds.

        Input is done by swiping a ID card (or otherwise inputting a
        valid sequence). 

        Output is done by spawning a shop user database lookup.
    """

    def __init__(self, event_q):
        super(IdLogger, self).__init__()

        self._event_q = event_q
        self._id_buffer = collections.deque(maxlen=ID_READ_LENGTH)
        
    def run(self):
        hook_manager = pyHook.HookManager()
        hook_manager.KeyDown = self._on_keyboard_event
        hook_manager.HookKeyboard()
        pythoncom.PumpMessages()

    def _on_keyboard_event(self, event_data):
        buffer_as_string = self._update_buffer(chr(event_data.Ascii))

        search_result = re.search(ID_REGEX, buffer_as_string)

        if search_result is not None:
            id_number = search_result.group()[2:-2]

            new_event = event.Event(event.CARD_SWIPE, id_number)
            event_logger.log_event_enqueue(new_event)
            self._event_q.put(new_event)

        return True  # Need to return true or HookManager will throw a fit.

    def _update_buffer(self, char):
        self._id_buffer.append(char)

        return ''.join(self._id_buffer)


def main():
    event_q = queue.Queue()
    IdLogger(event_q).run()


if __name__ == "__main__":
    main()