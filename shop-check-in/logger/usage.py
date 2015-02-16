from datetime import datetime
import util

LOG_DIRECTORY = "./logs/usage"
LOG_HEADER = 'In Time,Out Time,Machine,Name,Email'

POD_OPEN_MESSAGE = 'POD Opened the Shop'
POD_CLOSE_MESSAGE = 'POD Closed the Shop'
POD_ARRIVE_MESSAGE = 'POD Arrived at the Shop'
POD_EXIT_MESSAGE = 'POD Left the Shop'


def log_user_exit(user, start_time, machine):
    end_time = util.datetime_as_time_string(datetime.now())
    start_time = util.datetime_as_time_string(start_time)
    name = user.name
    email = user.email
    log_mesage = '%s,%s,%s,%s,%s' % (start_time, end_time, machine, name, email)
    util.log(log_mesage, LOG_HEADER, LOG_DIRECTORY)


def log_pod_opens_shop(user):
    _log_pod_event(user, POD_OPEN_MESSAGE)


def log_pod_closes_shop(user):
    _log_pod_event(user, POD_CLOSE_MESSAGE)


def log_pod_arrives_at_shop(user):
    _log_pod_event(user, POD_ARRIVE_MESSAGE)


def log_pod_exits_shop(user):
    _log_pod_event(user, POD_EXIT_MESSAGE)


def _log_pod_event(user, pod_event):
    start_time = end_time = util.datetime_as_time_string(datetime.now())
    machine = pod_event
    name = user.name
    email = user.email
    log_mesage = '%s,%s,%s,%s,%s' % (start_time, end_time, machine, name, email)
    util.log(log_mesage, LOG_HEADER, LOG_DIRECTORY)
