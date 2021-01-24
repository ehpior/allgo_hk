#-*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import datetime

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

    def btn_clicked(self):
        ret = self.ocx.dynamicCall("GetCodeListByMarket(QString)", ["0"])

        ret = ret.split(';')
        print("clicked")

        self.SetRealReg("1001", "005930", "202;204;206;208;210;212;213;214;215;216", 0)
        #self.SetRealReg("1000", ';'.join(ret[0:100]), "20;10", 0)
        #self.SetRealReg("1001", ';'.join(ret[100:200]), "20;10", 0)
        #self.SetRealReg("1002", ';'.join(ret[200:300]), "20;10", 0)
        #self.SetRealReg("1003", ';'.join(ret[300:400]), "20;10", 0)
        #self.SetRealReg("1004", ';'.join(ret[400:500]), "20;10", 0)
        #self.SetRealReg("1000", "000020;000040;000050;000060;000070;000075;000080;000087;000100;000105;000120;000140;000145;000150;000155;000157;000180;000210;000215;000220;000225;000227;000230;000240;000270;000300;000320;000325;000370;000390;000400;000430;", "20;10", 0)

    def btn2_clicked(self):
        #self.DisConnectRealData("1000")
        self.SetRealReg("2001", "005930", "20;10;25;11;12;13;202;204;206;210;212;213;214;215;216", 0)
        #self.ocx.dynamicCall("SetInputValue(QString, QString)", "시간일자구분", "1")
        #self.ocx.dynamicCall("SetInputValue(QString, QString)", "금액수량구분", "1")
        #self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005930")
        #self.ocx.dynamicCall("SetInputValue(QString, QString)", "날짜", "20210112")
        #self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "opt90008_req", "opt90008", 0, "0101")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt90008_req":
            print("opt90008_req")
            #name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "시간")
            #volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")

            #print(name)
            #print(volume)

    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")

    def _handler_login(self, err_code):
        if err_code == 0:
            self.statusBar().showMessage("login 완료")


    def _handler_real_data(self, code, real_type, data):
        if real_type == "주식체결":
            # 체결 시간
            #print(data)
            time =  self.GetCommRealData(code, 20)
            date = datetime.datetime.now().strftime("%Y-%m-%d ")
            time =  datetime.datetime.strptime(date + time, "%Y-%m-%d %H%M%S")
            #print(code, end=" ")
            #print(time, end=" ")
            # 현재가
            price =  self.GetCommRealData(code, 10)
            #print(int(price))

            with open("data/" + str(code) + ".txt", "a", encoding='utf8') as f:
                f.write(code+" "+time.strftime("%Y-%m-%d %H%M%S")+" "+price+"\n")

        if real_type == "종목프로그램매매":  ##   ' won' 금액    →   단위당 백만원
            print("종목프로그램매매")
            #name = self.code_to_name[code]
            timess = self.GetCommRealData(code, 20)
            sell_vol = self.GetCommRealData(code, 202)
            sell_won = self.GetCommRealData(code, 204)
            buy_vol = self.GetCommRealData(code, 206)
            buy_won = self.GetCommRealData(code, 208)
            Net_vol = self.GetCommRealData(code, 210)
            Net_won = self.GetCommRealData(code, 212)
            print(self.GetCommRealData(code, 212))

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