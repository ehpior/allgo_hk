from pykiwoom.kiwoom import *
import datetime
import time

def stockData(kiwoom, code):
    # 로그인
    #kiwoom = Kiwoom()
    #kiwoom.CommConnect()

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

    #out_name = f"{code}.xlsx"
    #print(df)
    #print("["+df['종목코드'][1]+"]")
    #df.to_excel(out_name)
    #time.sleep(3.6)

    return df
