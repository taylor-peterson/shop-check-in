import datetime
import util
import event


LOG_DIRECTORY = './logs/all_events'
LOG_HEADER = 'Begin Log'
EXTENSION = '.log'

def log_event_dequeue(event_):
    key = event_.key
    name = event.EVENT_CODE_TO_NAME_MAP[event_.key]
    data = event_.data
    log_message = 'Event   Pickup; name: %s ,key: %s, data %s' % (name, key, data)
    util.date_time_log(log_message, LOG_HEADER, LOG_DIRECTORY)


def log_event_enqueue(event_):
    key = event_.key
    name = event.EVENT_CODE_TO_NAME_MAP[event_.key]
    data = event_.data
    log_message = 'Event   Submit; name: %s ,key: %s, data %s' % (name, key, data)
    util.date_time_log(log_message, LOG_HEADER, LOG_DIRECTORY)


def log_send_message(message):
    log_message = 'Message Pickup; message: %s' % message.replace('\n','\\n')
    util.date_time_log(log_message, LOG_HEADER, LOG_DIRECTORY)


def log_display_message(message):
    log_message = 'Message Submit; message: %s' % message.replace('\n','\\n')
    util.date_time_log(log_message, LOG_HEADER, LOG_DIRECTORY)

