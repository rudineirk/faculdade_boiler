__all__ = [
    'WaterColumnController',
    'WaterTempController',
]

KC_LEVEL = 1200.0
HREF = 1.5

WATER_CAPACITANCE = 50000000.0
KC_TEMP = 0.15 * WATER_CAPACITANCE
TREF = 50.0


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


class WaterTempController(BaseController):

    def __init__(self, conn, queue):
        super(WaterTempController, self).__init__(
            conn,
            queue,
            KC_TEMP,
            TREF,
        )

    def set_actuator_value(self, value):
        self.conn.heat_flux = value
