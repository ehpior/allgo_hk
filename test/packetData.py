from ctypes import *

class real_programData(Structure):
    _pack_ = 1
    _fields_ = [("code", c_char * 6),   #종목코드
                ("price", c_uint32),    #현재가
                ("volume", c_uint32),   #거래량
                ("amount", c_uint32),   #거래대금
                ("date", c_char * 8),   #일자
                ("open", c_uint32),     #시가
                ("high", c_uint32),     #고가
                ("low", c_uint32)]      #저가
    '''
    def __init__(self, a, b=2):
        super(real_programData, self).__init__(a, b)
    '''