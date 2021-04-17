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

def toFloat(item):
    result = 0.0
    try:
        result = float(item)
    except:
        pass
    return result

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real")
        self.setGeometry(300, 300, 300, 400)

        btn1 = QPushButton("getStockList", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn_getStockList)

        btn2 = QPushButton("registerRealData", self)
        btn2.move(20, 100)
        btn2.clicked.connect(self.btn_registerRealData)

        btn3 = QPushButton("testSendChegData", self)
        btn3.move(20, 160)
        btn3.clicked.connect(self.btn_testSendChegData)

        btn4 = QPushButton("testSendProgramData", self)
        btn4.move(20, 240)
        btn4.clicked.connect(self.btn_testSendProgramData)

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        self.ocx.OnReceiveTrData.connect(self.receive_trdata)
        self.CommmConnect()

        self.cheg_addr = ('10.211.55.2', 7777)
        self.program_addr = ('10.211.55.2', 8888)

        #tcp
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #udp
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        """
        self.s.bind(self.server_addr)
        print("bind with %s" % repr(self.server_addr))

        try:
            self.s.listen(3)
            self.conn, self.addr = self.s.accept()
        except:
            print("ERROR: Connection to %s refused" % repr(self.server_addr))
            sys.exit(1)

        print("accepted %s", self.addr)"""

    def btn_getStockList(self):
        self.ret = self.ocx.dynamicCall("GetCodeListByMarket(QString)", ["0"]).split(';')
        self.ret2 = self.ocx.dynamicCall("GetCodeListByMarket(QString)", ["10"]).split(';')

        self.stock_len1 = int(len(self.ret))
        self.stock_len2 = int(len(self.ret2))
        print(len(self.ret))
        print(len(self.ret2))

    def btn_registerRealData(self):

        print("clicked")

        self.SetRealReg("1000", ';'.join(self.ret[0:100]), "10;131", 0)
        self.SetRealReg("1001", ';'.join(self.ret[100:200]), "10;131", 0)
        self.SetRealReg("1002", ';'.join(self.ret[200:300]), "10;131", 0)
        self.SetRealReg("1003", ';'.join(self.ret[300:400]), "10;131", 0)
        self.SetRealReg("1004", ';'.join(self.ret[400:500]), "10;131", 0)
        self.SetRealReg("1005", ';'.join(self.ret[500:600]), "10;131", 0)
        self.SetRealReg("1006", ';'.join(self.ret[600:700]), "10;131", 0)
        self.SetRealReg("1007", ';'.join(self.ret[700:800]), "10;131", 0)
        self.SetRealReg("1008", ';'.join(self.ret[800:900]), "10;131", 0)
        self.SetRealReg("1009", ';'.join(self.ret[900:1000]), "10;131", 0)
        self.SetRealReg("1010", ';'.join(self.ret[1000:1100]), "10;131", 0)
        self.SetRealReg("1011", ';'.join(self.ret[1100:1200]), "10;131", 0)
        self.SetRealReg("1012", ';'.join(self.ret[1200:1300]), "10;131", 0)
        self.SetRealReg("1013", ';'.join(self.ret[1300:1400]), "10;131", 0)
        self.SetRealReg("1014", ';'.join(self.ret[1400:1500]), "10;131", 0)
        self.SetRealReg("1015", ';'.join(self.ret[1500:1577]), "10;131", 0)

        self.SetRealReg("1016", ';'.join(self.ret2[0:100]), "10;131", 0)
        self.SetRealReg("1017", ';'.join(self.ret2[100:200]), "10;131", 0)
        self.SetRealReg("1018", ';'.join(self.ret2[200:300]), "10;131", 0)
        self.SetRealReg("1019", ';'.join(self.ret2[300:400]), "10;131", 0)
        self.SetRealReg("1020", ';'.join(self.ret2[400:500]), "10;131", 0)
        self.SetRealReg("1021", ';'.join(self.ret2[500:600]), "10;131", 0)
        self.SetRealReg("1022", ';'.join(self.ret2[600:700]), "10;131", 0)
        self.SetRealReg("1023", ';'.join(self.ret2[700:800]), "10;131", 0)
        self.SetRealReg("1024", ';'.join(self.ret2[800:900]), "10;131", 0)
        self.SetRealReg("1025", ';'.join(self.ret2[900:1000]), "10;131", 0)
        self.SetRealReg("1026", ';'.join(self.ret2[1000:1100]), "10;131", 0)
        self.SetRealReg("1027", ';'.join(self.ret2[1100:1200]), "10;131", 0)
        self.SetRealReg("1028", ';'.join(self.ret2[1200:1300]), "10;131", 0)
        self.SetRealReg("1029", ';'.join(self.ret2[1300:1400]), "10;131", 0)
        self.SetRealReg("1030", ';'.join(self.ret2[1400:1498]), "10;131", 0)

        print("finished")

    def btn_testSendChegData(self):
        cheg_data = stockData.test_cheg_data(self.ret)

        self.s.sendto(cheg_data, self.cheg_addr)

    def btn_testSendProgramData(self):
        program_data = stockData.test_program_data(self.ret)

        self.s.sendto(program_data, self.program_addr)

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
            index = 0
            try:
                index = int(self.ret.index(code))
            except ValueError:
                index = int(int(self.stock_len1) + int(self.ret2.index(code)))
            stock_code = code.encode()
            time = (self.GetCommRealData(code, 20)).encode()
            price = float(self.GetCommRealData(code, 10))

            """change_price = toFloat((50000))
            increase_rate = toFloat((50000))
            sell_1 = float((50000))
            buy_1 = float((50000))
            volume = float((50000))
            cul_volume = float((50000))
            cul_amount = float((50000))
            open = float((50000))
            high = float((50000))
            low = float((50000))
            plus_minus = float((50000))
            a1 = float((50000))
            a2 = float((50000))
            a3 = float((50000))
            turn_over = float((50000))
            a4 = float((50000))
            volume_power = float((50000))
            capitalization = float((50000))
            market = float((50000))
            a5 = float((50000))
            high_time = float((50000))
            low_time = float((50000))"""
            change_price = toFloat(self.GetCommRealData(code, 11))
            increase_rate = toFloat(self.GetCommRealData(code, 12))
            sell_1 = toFloat(self.GetCommRealData(code, 27))
            buy_1 = toFloat(self.GetCommRealData(code, 28))
            volume = toFloat(self.GetCommRealData(code, 15))
            cul_volume = toFloat(self.GetCommRealData(code, 13))
            cul_amount = toFloat(self.GetCommRealData(code, 14))
            open = toFloat(self.GetCommRealData(code, 16))
            high = toFloat(self.GetCommRealData(code, 17))
            low = toFloat(self.GetCommRealData(code, 18))
            plus_minus = toFloat(self.GetCommRealData(code, 25))
            a1 = toFloat(self.GetCommRealData(code, 26))
            a2 = toFloat(self.GetCommRealData(code, 29))
            a3 = toFloat(self.GetCommRealData(code, 30))
            turn_over = toFloat(self.GetCommRealData(code, 31))
            a4 = toFloat(self.GetCommRealData(code, 32))
            volume_power = toFloat(self.GetCommRealData(code, 228))
            capitalization = toFloat(self.GetCommRealData(code, 311))
            market = toFloat(self.GetCommRealData(code, 290))
            a5 = toFloat(self.GetCommRealData(code, 691))
            high_time = toFloat(self.GetCommRealData(code, 567))
            low_time = toFloat(self.GetCommRealData(code, 568))

            cheg_hk = stockData.real_cheg(index, stock_code, time, price, change_price, increase_rate, sell_1, buy_1,
                                          volume, cul_volume, cul_amount, open, high, low, plus_minus,
                                          a1, a2, a3, turn_over, a4, volume_power, capitalization,
                                          market, a5, high_time, low_time)

            self.s.sendto(cheg_hk, self.cheg_addr)

        if real_type == "종목프로그램매매":  ##   ' won' 금액    →   단위당 백만원
            index = 0
            try:
                index = int(self.ret.index(code))
            except ValueError:
                index = int(int(self.stock_len1) + int(self.ret2.index(code)))
            stock_code = code.encode()
            time = (self.GetCommRealData(code, 20)).encode()
            """price = float((50000))
            plus_minus = float((50000))
            change_price = float((50000))
            increase_rate = float((50000))
            cul_volume = float((50000))
            sell_volume = float((50000))
            sell_amount = float((50000))
            buy_volume = float((50000))
            buy_amount = float((50000))
            net_buy_volume = float((50000))
            net_buy_amount = float((50000))
            a1 = float((50000))
            a2 = float((50000))
            market = float((50000))
            ticker = float((50000))"""
            price = toFloat(self.GetCommRealData(code, 10))
            plus_minus = toFloat(self.GetCommRealData(code, 25))
            change_price = toFloat(self.GetCommRealData(code, 11))
            increase_rate = toFloat(self.GetCommRealData(code, 12))
            cul_volume = toFloat(self.GetCommRealData(code, 13))
            sell_volume = toFloat(self.GetCommRealData(code, 202))
            sell_amount = toFloat(self.GetCommRealData(code, 204))
            buy_volume = toFloat(self.GetCommRealData(code, 206))
            buy_amount = toFloat(self.GetCommRealData(code, 208))
            net_buy_volume = toFloat(self.GetCommRealData(code, 210))
            net_buy_amount = toFloat(self.GetCommRealData(code, 212))
            a1 = toFloat(self.GetCommRealData(code, 213))
            a2 = toFloat(self.GetCommRealData(code, 214))
            market = toFloat(self.GetCommRealData(code, 215))
            ticker = toFloat(self.GetCommRealData(code, 216))

            program_hk = stockData.real_program(index, stock_code, time, price, plus_minus, change_price,
                                                increase_rate, cul_volume, sell_volume, sell_amount, buy_volume,
                                                buy_amount, net_buy_volume, net_buy_amount, a1, a2, market, ticker)

            self.s.sendto(program_hk, self.program_addr)

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