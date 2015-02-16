import os
import re
from datetime import datetime

EXTENSION = '.log'
TIME_HEADER = 'Log Time,'


def date_time_log(msg, header, log_root_path):
    now = datetime_as_time_string(datetime.now())
    msg_with_time = now + ',' + msg
    header_with_time = TIME_HEADER + header
    log(msg_with_time, header_with_time, log_root_path)


def log(msg, header, log_root_path):
    now = datetime.now()
    path = [log_root_path, str(now.year), str(now.month), str(now.day) + EXTENSION]
    _append_to_file_safe_with_header(path, msg + '\r\n', header + '\r\n')


def _append_to_file_safe_with_header(path, msg, header):
    if isinstance(path, list):
        path = apply(os.path.join, path)
    _make_path_safe(path)
    if not os.path.exists(path):
        with open(path, 'wb') as file_:
            file_.write(header)
    with open(path, 'ab') as file_:
        file_.write(msg)

def _make_path_safe(path):
    if not os.path.exists(path):
        head, tail = os.path.split(path)
        if not head == '':
            _make_path_safe(head)
        if not re.match('^.*\..+$', tail):
            _safe_mkdir(path)

def _safe_mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def datetime_as_time_string(time):
    return '%02d:%02d:%02d.%03d' % (time.hour, time.minute, time.second, time.microsecond / 1000)