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
