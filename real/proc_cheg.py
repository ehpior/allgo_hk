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

        #tcp
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #udp
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #self.s.bind(self.server_addr)
        #print("bind with %s" % repr(self.server_addr))

        """try:
            self.s.listen(3)
            self.conn, self.addr = self.s.accept()
        except:
            print("ERROR: Connection to %s refused" % repr(self.server_addr))
            sys.exit(1)"""

        #print("accepted %s", self.addr)

    def btn_clicked(self):

        print("clicked")

        """self.SetRealReg("1000", ';'.join(self.ret[0:100]), "10;131", 0)
        self.SetRealReg("1001", ';'.join(self.ret[100:200]), "10;131", 0)
        self.SetRealReg("1002", ';'.join(self.ret[200:300]), "10;131", 0)
        self.SetRealReg("1003", ';'.join(self.ret[300:400]), "10;131", 0)
        self.SetRealReg("1004", ';'.join(self.ret[400:500]), "10;131", 0)"""

        self.SetRealReg("1000", ';'.join(self.ret[0:100]), "10", 0)
        self.SetRealReg("1001", ';'.join(self.ret[100:200]), "10", 0)
        self.SetRealReg("1002", ';'.join(self.ret[200:300]), "10", 0)
        self.SetRealReg("1003", ';'.join(self.ret[300:400]), "10", 0)
        self.SetRealReg("1004", ';'.join(self.ret[400:500]), "10", 0)

        print("finished")

        """for i in range(5):
            hk = stockData.real_cheg(int(self.ret.index("005930")), "005930".encode(), "153099".encode(), int(i), int(2), int(3), int(4), int(5),
                                        int(6), int(7), int(8), int(9), int(10), int(11),
                                        "8".encode(), int(13), int(14), int(15), int(16), int(17),
                                        int(18), int(19), int(20), int(21), int(22), int(23))

            nsent = self.conn.send(hk)
            print("Send %d %d bytes" % (0, nsent))"""

    def btn2_clicked(self):
        self.ret = self.ocx.dynamicCall("GetCodeListByMarket(QString)", ["0"]).split(';')

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
        #print("receive")
        print(code)
        if real_type == "주식체결":
            index = int(self.ret.index(code))
            print(index)
            stock_code = code.encode()
            print(stock_code)
            time = (self.GetCommRealData(code, 20)).encode()
            print(time)
            price = int(self.GetCommRealData(code, 10))
            print("price")
            change_price = int(self.GetCommRealData(code, 11))
            print("change_price")
            print(self.GetCommRealData(code, 12))
            #increase_rate = int(self.GetCommRealData(code, 12))
            increase_rate = int(-1)
            print("increase_rate")
            sell_1 = int(self.GetCommRealData(code, 27))
            print("sell_1")
            buy_1 = int(self.GetCommRealData(code, 28))
            print("buy_1")
            volume = int(self.GetCommRealData(code, 15))
            print("volume")
            cul_volume = int(self.GetCommRealData(code, 13))
            print("cul_volume")
            cul_amount = int(self.GetCommRealData(code, 14))
            print("cul_amount")
            open = int(self.GetCommRealData(code, 16))
            print("open")
            high = int(self.GetCommRealData(code, 17))
            print("high")
            low = int(self.GetCommRealData(code, 18))
            print("low")
            print(self.GetCommRealData(code, 25))
            #plus_minus = (self.GetCommRealData(code, 25)).encode()
            plus_minus = "a".encode()
            print("plus_minus")
            a1 = int(self.GetCommRealData(code, 26))
            print("a1")
            a2 = int(self.GetCommRealData(code, 29))
            print("a2")
            print(self.GetCommRealData(code, 30))
            #a3 = int(self.GetCommRealData(code, 30))
            a3 = int(-1)
            print("a3")
            print(self.GetCommRealData(code, 31))
            #turn_over = int(self.GetCommRealData(code, 31))
            turn_over = int(-1)
            print("turn_over")
            a4 = int(self.GetCommRealData(code, 32))
            print("a4")
            print(self.GetCommRealData(code, 228))
            #volume_power = int(self.GetCommRealData(code, 228))
            volume_power = int(-1)
            print("volume_power")
            capitalization = int(self.GetCommRealData(code, 311))
            print("capitalization")
            market = int(self.GetCommRealData(code, 290))
            print("market")
            a5 = int(self.GetCommRealData(code, 691))
            print("a5")
            high_time = int(self.GetCommRealData(code, 567))
            print("high_time")
            low_time = int(self.GetCommRealData(code, 568))
            print("low_time")

            cheg_hk = stockData.real_cheg(index, stock_code, time, price, change_price, increase_rate, sell_1, buy_1,
                                          volume, cul_volume, cul_amount, open, high, low, plus_minus,
                                          a1, a2, a3, turn_over, a4, volume_power, capitalization,
                                          market, a5, high_time, low_time)
            print("cheg_hk..")
            #nsent = self.conn.send(cheg_hk)
            self.s.sendto(cheg_hk, ('192.168.56.1', 7777))
            #print("Send %d %d bytes" % (0, nsent))
            print("send..")

        if real_type == "종목프로그램매매":  ##   ' won' 금액    →   단위당 백만원
            index = int(self.ret.index(code))
            stock_code = code.encode()
            time = (self.GetCommRealData(code, 20)).encode()
            print(time)
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

            program_hk = stockData.real_program(index, stock_code, time, price, plus_minus, change_price, increase_rate,
                            cul_volume, sell_volume, sell_amount, buy_volume, buy_amount, net_buy_volume,
                            net_buy_amount, a1, a2, market, ticker)

            #nsent = self.conn2.send(program_hk)
            self.s.sendto(program_hk, ('192.168.56.1', 8888))
            #print("Send %d %d bytes" % (0, nsent))

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