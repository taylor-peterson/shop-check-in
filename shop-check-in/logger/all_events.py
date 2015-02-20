import event
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import util

LOG_PATH = './logs/all_events/'
LOG_NAME = 'events.log'
initialized = False
logger = None


def check_init(func):
    def new_func(*args):
        global initialized
        if not initialized:
            init()
        return apply(func, args)
    return new_func

@check_init
def log_event_dequeue(event_):
    global logger
    key = event_.key
    name = event.EVENT_CODE_TO_NAME_MAP[event_.key]
    data = event_.data
    logger.debug('Event    Pickup; name: %s ,key: %s, data %s' % (name, key, data))


@check_init
def log_event_enqueue(event_):
    global logger
    key = event_.key
    name = event.EVENT_CODE_TO_NAME_MAP[event_.key]
    data = event_.data
    logger.debug('Event    Submit; name: %s ,key: %s, data %s' % (name, key, data))

@check_init
def log_send_message(message):
    global logger
    logger.debug('Message  Submit; message: %s' % message.replace('\n','\\n'))

@check_init
def log_display_message(message):
    global logger
    logger.debug('Message Display; message: %s' % message.replace('\n','\\n'))

def init():
    global logger, initialized
    logger = logging.getLogger('all_events')
    logger.setLevel(logging.DEBUG)

    util._safe_mkdirs(LOG_PATH)

    handler = TimedRotatingFileHandler(os.path.join(LOG_PATH, LOG_NAME),
                                       when='midnight',
                                       interval=1,
                                       backupCount=60)
    formatter = logging.Formatter('%(asctime)s: %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    initialized = True