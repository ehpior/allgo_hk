import datetime
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
