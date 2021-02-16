import datetime
from ctypes import *
from struct import pack

def tr_opt10081(kiwoom, code):

    # 문자열로 오늘 날짜 얻기
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # 전 종목의 일봉 데이터
    df = kiwoom.block_request("opt10081",
                              종목코드=code,
                              기준일자=today,
                              수정주가구분=1,
                              output="주식일봉차트조회",
                              next=0)

    output = pack('<6s iii 8s iii', code.encode(), int(df['현재가'][0]),
                int(df['거래량'][0]), int(df['거래대금'][0]),
                df['일자'][0].encode(), int(df['시가'][0]),
                int(df['고가'][0]), int(df['저가'][0]))

    return output

class real_program(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("code", c_char * 6),
                ("time", c_char * 6),
                ("price", c_uint32),
                ("plus_minus", c_char),
                ("change_price", c_uint32),
                ("increase_rate", c_uint32),
                ("cul_volume", c_uint32),
                ("sell_volume", c_uint32),
                ("sell_amount", c_uint32),
                ("buy_volume", c_uint32),
                ("buy_amount", c_uint32),
                ("net_buy_volume", c_uint32),
                ("net_buy_amount", c_uint32),
                ("a1", c_uint32),
                ("a2", c_uint32),
                ("market", c_uint32),
                ("ticker", c_uint32)]

class real_cheg(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("code", c_char * 6),
                ("time", c_char * 6),
                ("price", c_uint32),
                ("change_price", c_uint32),
                ("increase_rate", c_uint32),
                ("sell_1", c_uint32),
                ("buy_1", c_uint32),
                ("volume", c_uint32),
                ("cul_volume", c_uint32),
                ("cul_amount", c_uint32),
                ("open", c_uint32),
                ("high", c_uint32),
                ("low", c_uint32),
                ("plus_minus", c_char),
                ("a1", c_uint32),
                ("a2", c_uint32),
                ("a3", c_uint32),
                ("turn_over", c_uint32),
                ("a4", c_uint32),
                ("volume_power", c_uint32),
                ("capitalization", c_uint32),
                ("market", c_uint32),
                ("a5", c_uint32),
                ("high_time", c_uint32),
                ("low_time", c_uint32)]

