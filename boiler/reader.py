from __future__ import print_function

from datetime import datetime
from time import sleep

__all__ = [
    'WaterColumnReader',
    'WaterTempReader',
]


class BaseReader(object):

    def __init__(self, conn, queue, loop_time=1000):
        self._conn = conn
        self._queue = queue
        self._loop_time = float(loop_time) / 1000.0
        self._last_loop = None

    def run(self):
        while True:
            value = self.read_value()
            self._queue.put(value)
            self.sleep()

    def read_value(self):
        raise NotImplementedError

    def sleep(self):
        time_now = datetime.now()
        if self._last_loop is None:
            self._last_loop = time_now
        time_diff = time_now - self._last_loop
        sleep_time = self._loop_time - time_diff.total_seconds()
        if sleep_time <= 0:
            sleep_time = self._loop_time
        self._last_loop = time_now
        sleep(sleep_time)


class WaterColumnReader(BaseReader):

    def read_value(self):
        value = self._conn.water_column
        print('Reader Water: {0}'.format(value))
        return value


class WaterTempReader(BaseReader):

    def read_value(self):
        value = self._conn.water_inside_temp
        print('Reader Temp: {0}'.format(value))
        return value
