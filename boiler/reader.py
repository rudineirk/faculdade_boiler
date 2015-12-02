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
            self.queue.put(value)
            self.sleep()

    def read_value(self):
        raise NotImplementedError

    def sleep(self):
        if self._last_loop is None:
            self._last_loop = datetime.now()
        time_diff = datetime.now() - self._last_loop
        sleep_time = self._loop_time - time_diff.total_seconds()
        self._last_loop = datetime.now()
        sleep(sleep_time)


class WaterColumnReader(BaseReader):

    def read_value(self):
        return self._conn.water_column


class WaterTempReader(BaseReader):

    def read_value(self):
        return self._conn.water_inside_temp
