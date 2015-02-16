import os
import datetime

LOG_DIRECTORY = "."
EXTENSION = '.log'
HEADER = 'Log Time,'


def log_event(msg, header):
    now = datetime.datetime.now()
    path = [LOG_DIRECTORY, str(now.year), str(now.month), str(now.day) + EXTENSION]
    msg_with_time = str(now) + ',' + msg + '\r\n'
    header_with_time = HEADER + header + '\r\n'
    _append_to_path(path, msg_with_time, header_with_time)


def _append_to_path(path, msg, header):
    if isinstance(path, str):
        path = _split_path_to_list(path)
    if isinstance(path, list):
        text_path = apply(os.path.join, path)
        assert '.' in path[-1]
        _create_path_dir(path[:-1])
        print path
        if not os.path.exists(text_path):
            with open(text_path, 'wb') as file_:
                file_.write(header)
        with open(text_path, 'ab') as file_:
            file_.write(msg)


def _create_path_dir(path):
    if isinstance(path, list):
        for i in range(len(path)):
            print "Path to", path
            partial_path = apply(os.path.join, [LOG_DIRECTORY] + path[0:i + 1])
            _safe_mkdir(partial_path)
    elif isinstance(path, str):
        _create_path_dir(_split_path_to_list(path))
    else:
        print "Path %s not recognized" % path
        assert False


def _safe_mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def _split_path_to_list(path):
    if '/' in path:
        return path.split('/')
    elif '\\' in path:
        return path.split('\\')
    else:
        return [path]
