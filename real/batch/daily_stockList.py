import pymysql
from pykiwoom.kiwoom import *

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

# mysql CRUD : https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

class Kiwoom(QAxWidget):  # QAxWidget 클래스로부터 dynamicCall, setControl, OnEventConnect 를 상속받음
    def __init__(self):
        super().__init__()
        self.db = pymysql.connect(
            user='jhk',
            passwd='wjdgusrl34',
            host='192.168.0.10',
            db='allgo',
            charset='utf8'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

        self._create_kiwoom_instance()  # 키움증권 OpenAPI 를 정상적으로 사용할 수 있도록 처리함
        self._set_signal_slots()        # 이벤트 처리메소드 등록


    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")      # 이거 대신 obj = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1") 가능

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)  # 콜백함수 등록

    def _event_connect(self, err_code):
        if err_code == 0:
            print("로그인 성공")
        else:
            print("로그인 에러코드 : " + str(err_code))

        self.login_event_loop.exit()

    def comm_connect(self):
        self.dynamicCall("CommConnect()")    # 로그인창 띄우기
        self.login_event_loop = QEventLoop() # 이벤트 루프 생성
        self.login_event_loop.exec_()        # 프로그램 흐름을 일시중지하고 이벤트만 처리할 수 있는 상태로 만듬

    def get_all_codes_names(self):
        kospi_code_list = self.dynamicCall("GetCodeListByMarket(QString)", ["0"]).split(';')
        kospi_code_name_list = []

        kosdaq_code_list = self.dynamicCall("GetCodeListByMarket(QString)", ["10"]).split(';')
        kosdaq_code_name_list = []

        for index, code in enumerate(kospi_code_list):
            name = self.dynamicCall("GetMasterCodeName(QString)", [code])  # 맨뒤는 종목코드, 코드에 따른 종목명을 가져옴
            if not (code and name):
                continue
            kospi_code_name_list.append(tuple([index, code, name, "0"]))

        for index, code in enumerate(kosdaq_code_list):
            name = self.dynamicCall("GetMasterCodeName(QString)", [code])  # 맨뒤는 종목코드, 코드에 따른 종목명을 가져옴
            if not (code and name):
                continue
            kosdaq_code_name_list.append(tuple([index, code, name, "10"]))

        for item in kospi_code_name_list:
            print(item)

        sql = "insert into STOCK_LIST values(%s, %s, %s, %s)"
        self.cursor.executemany(sql, kospi_code_name_list)
        self.cursor.executemany(sql, kosdaq_code_name_list)
        self.db.commit()

        exit(0)


if __name__ == "__main__":
    '''
    Kiwoom 클래스는 QAxWiget 클래스를 상속받았기 때문에
    Kiwoom 클래스에 대한 인스턴스를 생성하려면 먼저 QApplication 클래스의 인스턴스를 생성해야함
    '''
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()
    kiwoom.get_all_codes_names()
    sys.exit(app.exec_())