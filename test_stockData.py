#!/usr/bin/env python

""" client.py - Echo client for sending/receiving C-like structs via socket
References:
- Ctypes fundamental data types: https://docs.python.org/2/library/ctypes.html#ctypes-fundamental-data-types-2
- Ctypes structures: https://docs.python.org/2/library/ctypes.html#structures-and-unions
- Sockets: https://docs.python.org/2/howto/sockets.html
"""

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


def testhk():
    kiwoom = Kiwoom()
    kiwoom.CommConnect()

    server_addr = ('192.168.0.3', 8888)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #if s < 0:
    #    print("Error creating socket")

    try:
        s.connect(server_addr)
        print("Connected to %s" % repr(server_addr))
    except:
        print("ERROR: Connection to %s refused" % repr(server_addr))
        sys.exit(1)

    try:
        buff = s.recv(10)
        print("start")
        print(buff)
        print(buff.decode())
        buff = buff.decode()
        print("end")

        print("")
        df = stockData.stockData(kiwoom, buff)

        #for i in range(len(df.index)):
        for i in range(3):
            opt10081_hk = opt10081(i, buff.encode(), int(df['거래량'][i]), int(df['거래대금'][i]), int(df['일자'][i]), int(df['시가'][i]), int(df['고가'][i]), int(df['저가'][i]))
            #print(sizeof(opt10081_hk))
            nsent = s.send(opt10081_hk)
            print("Send %d %d bytes" % (i, nsent))
            #print("")

    finally:
        print("Closing socket")
        s.close()


if __name__ == "__main__":
    testhk()