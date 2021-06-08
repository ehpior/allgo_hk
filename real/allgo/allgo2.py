import datetime

import pymysql
import sys


# mysql CRUD : https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

print("--------------")
print(datetime.datetime.now())

if len(sys.argv) != 2:
    print('argv error')
    exit(1)

today = sys.argv[1]
#today = '20210521'
if len(today) != 8:
    print('len(today) error')
    exit(1)

db = pymysql.connect(
    user='jhk',
    passwd='wjdgusrl34',
    host='1.240.167.231',  # '10.211.55.2',
    db='allgo',
    charset='utf8'
)

#cursor = db.cursor(pymysql.cursors.DictCursor)
#cursor = db.cursor(pymysql.cursors.Cursor)

scores = list()

with db.cursor(pymysql.cursors.Cursor) as cursor:

    ### 날짜 검사 시작

    sql = """select ifnull(max(date), 0) from ag_score where type='B' and date <= %s"""

    cursor.execute(sql, [today])
    maxDate_score = cursor.fetchone()[0]

    sql = """select ifnull(max(date), 0) from stock_program where date <= %s"""

    cursor.execute(sql, [today])
    maxDate_stock = cursor.fetchone()[0]

    print(f"type : B, today : {today}, maxDate_stock : {maxDate_stock}, maxDate_score : {maxDate_score}")

    if (today != maxDate_stock) or (maxDate_stock <= maxDate_score) or (maxDate_stock == 0):
        print("date error")
        exit(1)

    ### 알고리즘 시작

    sql = """SELECT a.CODE, a.net_buy_amount, b.capitalization
        FROM stock_program a
            INNER JOIN stock_cheg b ON b.date = a.date AND b.code = a.code
        WHERE a.date = %s"""

    cursor.execute(sql, [today])

    for elem in cursor.fetchall():
        tmp_code = elem[0]
        tmp_net_buy_amount = float(elem[1])
        tmp_capitalization = float(elem[2])

        scores.append((tmp_code, tmp_net_buy_amount / tmp_capitalization * 100))


scores = sorted(scores, key=lambda x: x[1], reverse=True)

final_scores = list()

for idx, (code, score) in enumerate(scores):
    # 랭크, 종목코드, 타입, 점수
    final_score = (today, 'B', code, round(score, 2), idx+1)
    final_scores.append(final_score)

print(f"final_scores : {len(final_scores)}")

with db.cursor(pymysql.cursors.Cursor) as cursor:
    sql = "insert into ag_score(date, type, code, score, rank) values(%s, %s, %s, %s, %s)"
    cursor.executemany(sql, final_scores)
    db.commit()

db.close()