__all__ = [
    'WaterColumnController',
]

KC_LEVEL = 1200.0
HREF = 1.5


class BaseController(object):

    def __init__(self, conn, queue, kc, ref):
        self.conn = conn
        self._queue = queue
        self.kc = kc
        self.ref = ref

    def get_sensor_value(self):
        return self.queue.get()

    def run(self):
        value = self.get_sensor_value()
        value = self.kc * (self.ref * value)
        self.set_actuator(value)

    def set_actuator_value(self, value):
        raise NotImplementedError


class WaterColumnController(BaseController):

    def __init__(self, conn, queue):
        super(WaterColumnController, self).__init__(
            conn,
            queue,
            KC_LEVEL,
            HREF,
        )

    def set_actuator_value(self, value):
        self.conn.water_flux = value
