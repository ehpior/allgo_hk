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
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from ctypes import *

""" This class defines a C-like struct """

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real")
        self.setGeometry(300, 300, 300, 400)

        btn = QPushButton("Register", self)
        btn.move(20, 20)
        btn.clicked.connect(self.btn_clicked)

        btn2 = QPushButton("DisConnect", self)
        btn2.move(20, 100)
        btn2.clicked.connect(self.btn2_clicked)

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        self.ocx.OnReceiveTrData.connect(self.receive_trdata)
        self.CommmConnect()

        self.server_addr = ('192.168.0.26', 8888)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.server_addr)
        print("bind with %s" % repr(self.server_addr))

        try:
            self.s.listen(3)
            #self.conn, self.addr = self.s.accept()
        except:
            print("ERROR: Connection to %s refused" % repr(self.server_addr))
            sys.exit(1)

        #print("accepted %s", self.addr)

    def btn_clicked(self):

        print("clicked")

        """self.SetRealReg("1000", ';'.join(ret[0:100]), "10;131", 0)
        self.SetRealReg("1001", ';'.join(ret[100:200]), "10;131", 0)
        self.SetRealReg("1002", ';'.join(ret[200:300]), "10;131", 0)
        self.SetRealReg("1003", ';'.join(ret[300:400]), "10;131", 0)
        self.SetRealReg("1004", ';'.join(ret[400:500]), "10;131", 0)"""

        for i in range(5):
            hk = stockData.real_cheg(int(self.ret.index("005930")), "005930".encode(), "153099".encode(), int(i), int(2), int(3), int(4), int(5),
                                        int(6), int(7), int(8), int(9), int(10), int(11),
                                        "8".encode(), int(13), int(14), int(15), int(16), int(17),
                                        int(18), int(19), int(20), int(21), int(22), int(23))

            nsent = self.conn.send(hk)
            print("Send %d %d bytes" % (0, nsent))

    def btn2_clicked(self):
        self.ret = self.ocx.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        with open('../real/codes.txt', 'w') as f:
            f.write(self.ret)
        self.ret = self.ret.split(';')

        print(self.ret)
        print(self.ret.index("005930"))
        print(len(self.ret))

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt90008_req":
            print("opt90008_req")
            #name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "시간")
            #volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")

    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")

    def _handler_login(self, err_code):
        if err_code == 0:
            self.statusBar().showMessage("login 완료")

    def _handler_real_data(self, code, real_type, data):
        if real_type == "주식체결":
            time = (self.GetCommRealData(code, 20)).encode()
            price = int(self.GetCommRealData(code, 10))
            change_price = int(self.GetCommRealData(code, 21))
            increase_rate = int(self.GetCommRealData(code, 12))
            sell_1 = int(self.GetCommRealData(code, 27))
            buy_1 = int(self.GetCommRealData(code, 28))
            volume = int(self.GetCommRealData(code, 15))
            cul_volume = int(self.GetCommRealData(code, 13))
            cul_amount = int(self.GetCommRealData(code, 14))
            open = int(self.GetCommRealData(code, 16))
            high = int(self.GetCommRealData(code, 17))
            low = int(self.GetCommRealData(code, 18))
            plus_minus = (self.GetCommRealData(code, 25)).encode()
            a1 = int(self.GetCommRealData(code, 26))
            a2 = int(self.GetCommRealData(code, 29))
            a3 = int(self.GetCommRealData(code, 30))
            turn_over = int(self.GetCommRealData(code, 31))
            a4 = int(self.GetCommRealData(code, 32))
            volume_power = int(self.GetCommRealData(code, 228))
            capitalization = int(self.GetCommRealData(code, 311))
            market = int(self.GetCommRealData(code, 290))
            a5 = int(self.GetCommRealData(code, 691))
            high_time = int(self.GetCommRealData(code, 567))
            low_time = int(self.GetCommRealData(code, 568))

            cheg_hk = stockData.real_cheg(time, price, change_price, increase_rate, sell_1, buy_1,
                      volume, cul_volume, cul_amount, open, high, low, plus_minus,
                      a1, a2, a3, turn_over, a4, volume_power, capitalization,
                      market, a5, high_time, low_time)

            nsent = self.conn.send(cheg_hk)
            print("Send %d %d bytes" % (0, nsent))

        if real_type == "종목프로그램매매":  ##   ' won' 금액    →   단위당 백만원
            time = (self.GetCommRealData(code, 20)).encode()
            price = int(self.GetCommRealData(code, 10))
            plus_minus = (self.GetCommRealData(code, 25)).encode()
            change_price = int(self.GetCommRealData(code, 11))
            increase_rate = int(self.GetCommRealData(code, 12))
            cul_volume = int(self.GetCommRealData(code, 13))
            sell_volume = int(self.GetCommRealData(code, 202))
            sell_amount = int(self.GetCommRealData(code, 204))
            buy_volume = int(self.GetCommRealData(code, 206))
            buy_amount = int(self.GetCommRealData(code, 208))
            net_buy_volume = int(self.GetCommRealData(code, 210))
            net_buy_amount = int(self.GetCommRealData(code, 212))
            a1 = int(self.GetCommRealData(code, 213))
            a2 = int(self.GetCommRealData(code, 214))
            market = int(self.GetCommRealData(code, 215))
            ticker = int(self.GetCommRealData(code, 216))

            program_hk = stockData.real_program(time, price, plus_minus, change_price, increase_rate,
                            cul_volume, sell_volume, sell_amount, buy_volume, buy_amount, net_buy_volume,
                            net_buy_amount, a1, a2, market, ticker)

            nsent = self.conn.send(program_hk)
            print("Send %d %d bytes" % (0, nsent))

    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                              screen_no, code_list, fid_list, real_type)

    def DisConnectRealData(self, screen_no):
        self.ocx.dynamicCall("DisConnectRealData(QString)", screen_no)

    def GetCommRealData(self, code, fid):
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid)
        return data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()