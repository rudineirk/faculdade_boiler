from queue import Queue
from threading import Thread

from .conn import BoilerConn
from .controller import WaterColumnController, WaterTempController
from .reader import WaterColumnReader, WaterTempReader


class Main(object):

    def __init__(self):
        self._threads = []
        self.column_queue = Queue()
        self.temp_queue = Queue()

        self.conn = BoilerConn()

        self.column_controller = WaterColumnController(
            self.conn,
            self.column_queue,
        )
        self.temp_controller = WaterTempController(
            self.conn,
            self.temp_queue,
        )

        self.column_reader = WaterColumnReader(
            self.conn,
            self.column_queue,
            loop_time=2000,
        )
        self.temp_reader = WaterTempReader(
            self.conn,
            self.temp_queue,
            loop_time=1500,
        )

    def make_threads(self):
        self._threads.append(Thread(target=self.column_controller.run))
        self._threads.append(Thread(target=self.temp_controller.run))
        self._threads.append(Thread(target=self.column_reader.run))
        self._threads.append(Thread(target=self.temp_reader.run))

    def run(self):
        self.make_threads()
        for thread in self._threads:
            thread.start()

        for thread in self._threads:
            thread.join()
        self.conn.close()


if __name__ == '__main__':
    main = Main()
    main.run()
