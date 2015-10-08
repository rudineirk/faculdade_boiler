import time


class PID:
    def __init__(self):
        self.Kp = 0
        self.Kd = 0
        self.Ki = 0
        self.initialize()

    def set_kp(self, Kp):
        self.Kp = Kp

    def set_ki(self, Ki):
        self.Ki = Ki

    def set_kd(self, Kd):
        self.Kd = Kd

    def set_prev_err(self, preverr):
        self.prev_err = preverr

    def initialize(self):
        self.currtm = time.time()
        self.prevtm = self.currtm
        self.prev_err = 0
        self.Cp = 0
        self.Ci = 0
        self.Cd = 0

    def run(self, error):
        """
        Performs a PID computation and returns a control value based on the
        elapased time (dt) and the error signal from a summing junction.
        """

        self.currtm = time.time()       # get t
        dt = self.currtm - self.prevtm  # get delta t
        de = error - self.prev_err      # get delta error

        self.Cp = self.Kp * error   # proportional term
        self.Ci += error * dt       # integral term

        self.Cd = 0
        if dt > 0:                  # no div by zero
            self.Cd = de/dt         # derivative term

        self.prevtm = self.currtm   # save t for next pass
        self.prev_err = error       # save t-1 error

        return self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)
