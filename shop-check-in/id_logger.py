import re  # Regular expressions
import threading

import pyHook  # Callbacks for keyboard events
import pythoncom  # Tie in to Windows events

ID_REGEX = ";[0-9]{10}\x00"


class IdLogger(threading.Thread):
    """ Listens to keyboard input and reports any properly formatted
        IDs that it finds.

        Input is done by swiping a ID card (or otherwise inputting a
        valid sequence). 

        Output is done by spawning a shop user database lookup.
    """

    def __init__(self, shop_user_database):        
        super(IdLogger, self).__init__()

        self._shop_user_database = shop_user_database
        self._id_buffer = []
        
    def run(self):
        hook_manager = pyHook.HookManager()
        hook_manager.KeyDown = self._on_keyboard_event
        hook_manager.HookKeyboard()
        pythoncom.PumpMessages()

    def _on_keyboard_event(self, event):
        self._add_char_to_buffer(chr(event.Ascii))
        buffer_as_string = ''.join(map(str, self._id_buffer))
        
        search_result = re.search(ID_REGEX, buffer_as_string)
        
        if search_result is not None:
            id_number = search_result.group()[2:-2]
            
            t = threading.Thread(target=self._shop_user_database.get_shop_user, args=(id_number, ))
            t.start()
            
        return True

    def _add_char_to_buffer(self, char):
        if len(self._id_buffer) >= 12:
            del self._id_buffer[0]

        self._id_buffer.append(char)
