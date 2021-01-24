#!/usr/bin/env python

""" client.py - Echo client for sending/receiving C-like structs via socket
References:
- Ctypes fundamental data types: https://docs.python.org/2/library/ctypes.html#ctypes-fundamental-data-types-2
- Ctypes structures: https://docs.python.org/2/library/ctypes.html#structures-and-unions
- Sockets: https://docs.python.org/2/howto/sockets.html
"""

#얘가 server이고 c가 client일때

import socket
import sys
import random
import stockData
from pykiwoom.kiwoom import *
from ctypes import *


""" This class defines a C-like struct """
class Payload(Structure):
    _fields_ = [("id", c_uint32),
                ("counter", c_uint32),
                ("temp", c_float),("temp2", c_float)]

class opt10081(Structure):
    _fields_ = [("idx", c_uint32),
                ("code", c_char * 6),
                ("vol", c_uint32),
                ("amt", c_uint32),
                ("date", c_uint32),
                ("open", c_uint32),
                ("high", c_uint32),
                ("low", c_uint32)]

class opt10082(Structure):
    _fields_ = [("code", c_char * 6),   #종목코드
                ("price", c_uint32),    #현재가
                ("volume", c_uint32),   #거래량
                ("amount", c_uint32),   #거래대금
                ("date", c_char * 8),   #일자
                ("open", c_uint32),     #시가
                ("high", c_uint32),     #고가
                ("low", c_uint32)]      #저가


def testhk():
    kiwoom = Kiwoom()
    kiwoom.CommConnect()

    server_addr = ('192.168.0.26', 8888)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(server_addr)
    print("bind with %s" % repr(server_addr))
    while 1:

        try:
            s.listen(3)
            conn, addr = s.accept()
        except:
            print("ERROR: Connection to %s refused" % repr(server_addr))
            sys.exit(1)

        try:
            buff = conn.recv(10)
            print("start")
            buff = buff.decode()
            print("end")

            print("")
            df = stockData.stockData(kiwoom, buff)

            opt10082_hk = opt10082(buff.encode(), int(df['현재가'][0]), int(df['거래량'][0]), int(df['거래대금'][0]),
                                   df['일자'][0].encode(), int(df['시가'][0]), int(df['고가'][0]), int(df['저가'][0]))

            nsent = conn.send(opt10082_hk)
            print("Send %d %d bytes" % (0, nsent))

        finally:
            print("Closing socket")
            conn.close()


if __name__ == "__main__":
    testhk()