import flask
import shop
import shop_user
import datetime
import time
import slots
import threading

"""
Status dictionary format
status =
{
open: True,
pods: '...',
wood: {'machines': {'name':
                  {'in use': True,
                   'users': '...',
                   'start time': '...'}
                  }
      'limbo': ['...', '...', ]
},
main:{...},
sheet: {...}
}
"""


class LiveSite(object):
    def __init__(self, shop):
        self._server = flask.Flask('website')
        self._server.config.from_pyfile('web.cfg')
        self._shop = shop
        self._shop_status = {}
        self.daemon = False

        @self._server.route('/')
        def basic():
            self.build_shop_status()
            return flask.render_template('status.html', status=self._shop_status)

    @staticmethod
    def _datetime_as_time_string(time_):
        if not time_:
            return ""
        return time_.strftime('%I:%M %p')

    @staticmethod
    def build_machine_status_dict(user_s, start_time):
        users_names = ', '.join([user.name for user in user_s])
        start_time = LiveSite._datetime_as_time_string(start_time)
        return {'in_use': (users_names != ''), 'users': users_names, 'start_time': start_time}

    def build_shop_status(self):
        self._shop_status = {'open': self._shop.is_open()}
        if self._shop.is_open():
            pods = ', '.join([user.name for user in self._shop.pods()])
            self._shop_status['pods'] = pods
            self._add_machines_to_shop_status_dict()

    def _add_machines_to_shop_status_dict(self):
        self._shop_status['wood'] = {'machines': {}, 'limbo': []}
        self._shop_status['main'] = {'machines': {}, 'limbo': []}
        self._shop_status['sheet'] = {'machines': {}, 'limbo': []}

        for slot in slots.SLOTS:
            sub_shop = slots.which_sub_shop(slot)
            if sub_shop:
                self._add_machine_to_sub_shop_status(slot, sub_shop)

    def _add_machine_to_sub_shop_status(self, slot, sub_shop):
        if slots.is_specific_machine(slot):
            machine_name = self._shop.machine_name(slot)
            user_s = self._shop.current_machine_user_s(slot)
            start_time = self._shop.current_machine_start_time(slot)
            machine_status = self.build_machine_status_dict(user_s, start_time)
            self._shop_status[sub_shop]['machines'][machine_name] = machine_status
        else:
            if self._shop.is_machine_in_use(slot):
                user_s_names = [user.name for user in self._shop.current_machine_user_s(slot)]
                self._shop_status[sub_shop]['limbo'] += user_s_names

    def start(self):
        if self.daemon:
            daemon = threading.Thread(target=self._start)
            daemon.start()
        else:
            self._start()

    def _start(self):
        self._server.run(host='0.0.0.0',
                         port=80)
