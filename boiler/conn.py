#!/usr/bin/python3

from __future__ import print_function

import socket

MSG_AIR_TEMP = b"sta0"
MSG_WATER_INSIDE_TEMP = b"st-0"
MSG_WATER_IN_TEMP = b"sti0"
MSG_WATER_OUT_TEMP = b"sno0"
MSG_WATER_COLUMN = b"sh-0"
CMD_HEAT_FLUX = b"aq"
CMD_WATER_FLUX = b"ani"


class BoilerConn(object):
    def __init__(self, host="127.0.0.1", port=4545):
        self.host = host
        self.port = port
        self.sock = None
        self._heat_flux = 0.0
        self._water_flux = 0.0
        self.open()

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def close(self):
        self.sock.close()

    def _send(self, msg):
        return self.sock.sendto(msg, (self.host, self.port))

    def _read(self, size=10000):
        return self.sock.recv(size)

    def _set_cmd(self, cmd, value):
        # Transforma valor em bytes
        value = str(value).encode()
        self._send(cmd + value + b"\r\n")
        self._read()

    def _get_msg(self, msg):
        self._send(msg)
        data = self._read()
        # Transforma bytes em string
        data = data.decode("utf-8")
        data = data[3:].replace(",", ".").strip()
        return float(data)

    @property
    def heat_flux(self):
        return self._heat_flux

    @heat_flux.setter
    def heat_flux(self, value):
        self._heat_flux = value
        self._set_cmd(CMD_HEAT_FLUX, value)

    @property
    def water_flux(self):
        return self._water_flux

    @water_flux.setter
    def water_flux(self, value):
        self._water_flux = value
        self._set_cmd(CMD_WATER_FLUX, value)

    @property
    def air_temp(self):
        return self._get_msg(MSG_AIR_TEMP)

    @property
    def water_inside_temp(self):
        return self._get_msg(MSG_WATER_INSIDE_TEMP)

    @property
    def water_in_temp(self):
        return self._get_msg(MSG_WATER_IN_TEMP)

    @property
    def water_out_temp(self):
        return self._get_msg(MSG_WATER_OUT_TEMP)

    @property
    def water_column(self):
        return self._get_msg(MSG_WATER_COLUMN)
