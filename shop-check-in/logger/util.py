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


def _safe_mkdirs(path):
    try:
        os.makedirs(_cut_file_name(path))
    except WindowsError:
        pass


def _append_to_file_safe_with_header(path, msg, header):
    if isinstance(path, list):
        path = apply(os.path.join, path)
    _safe_mkdirs(path)
    if not os.path.exists(path):
        with open(path, 'wb') as file_:
            file_.write(header)
    with open(path, 'ab') as file_:
        file_.write(msg)


def _cut_file_name(path):
    head, tail = os.path.split(path)
    if '.' in tail:
        return head
    else:
        return path


def datetime_as_time_string(time):
    return '%02d:%02d:%02d.%03d' % (time.hour, time.minute, time.second, time.microsecond / 1000)