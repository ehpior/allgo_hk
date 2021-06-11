import datetime

import pymysql
import sys

import redis

# mysql CRUD : https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

print("--------------")
print(datetime.datetime.now())

if len(sys.argv) != 2:
    print('argv error')
    exit(1)

today = sys.argv[1]

if len(today) != 8:
    print('len(today) error')
    exit(1)

db = pymysql.connect(
    user='jhk',
    passwd='wjdgusrl34',
    host='1.240.167.231',#'10.211.55.2',
    db='allgo',
    charset='utf8'
)

db_redis = redis.StrictRedis(host='1.240.167.231', port=6379, db=0, password='wjdgusrl34', charset="utf-8", decode_responses=True)
#cursor = db.cursor(pymysql.cursors.DictCursor)
#cursor = db.cursor(pymysql.cursors.Cursor)

businessDay_state = int(db_redis.get('businessDay_state'))

d_today = dict()

with db.cursor(pymysql.cursors.Cursor) as cursor:

    ### 날짜 검사 시작

    sql = """select ifnull(max(date), 0) from ag_score where type='A' and date <= %s"""

    cursor.execute(sql, [today])
    maxDate_score = cursor.fetchone()[0]

    sql = """select ifnull(max(date), 0) from stock_cheg where date <= %s"""

    cursor.execute(sql, [today])
    maxDate_stock = cursor.fetchone()[0]

    print(f"type : B, today : {today}, maxDate_stock : {maxDate_stock}, maxDate_score : {maxDate_score}")

    if (maxDate_stock != maxDate_score) or (businessDay_state != 3) or (maxDate_stock == 0) or (maxDate_score == 0):
        print("datetime error")
        exit(1)

    ### 알고리즘 시작

    sql = """SELECT a.code, d.name_kor, a.score, a.rank
        FROM ag_score a
            INNER JOIN (SELECT CODE, MAX(score) AS score
                FROM ag_score
                WHERE DATE >= IFNULL((SELECT DISTINCT(DATE)
                        FROM ag_score
                        WHERE DATE < %s
                        ORDER BY DATE desc
                        LIMIT 19, 1), 0)
                    AND DATE < %s
                    AND TYPE = 'B'
                GROUP BY CODE
                HAVING COUNT(1) = 20) b ON b.code = a.code AND b.score = a.score
            LEFT JOIN ag_portfolio c ON c.code = a.code AND c.`status` = 'H'
            INNER JOIN stock_list d ON d.code = a.code and d.market IN ('0', '10')
            INNER JOIN stock_cheg e on e.code = a.code and e.date = a.date and e.capitalization >= 3000
        WHERE a.date = (SELECT MAX(DATE) FROM ag_score where DATE < %s)
            AND a.type = 'B'
            AND c.code IS null
        ORDER BY a.rank asc"""

    args = [today, today, today]
    cursor.execute(sql, args)

    result = cursor.fetchall()

    if len(result) == 0:
        print("nothing")
        exit(1)

    d_today['code'] = str(result[0][0])
    d_today['stock_name'] = str(result[0][1])

d_today['price'] = float(db_redis.get('stock:' + d_today['code']))

today_stock = ('B', d_today['code'], d_today['stock_name'], today, abs(d_today['price']))

print(today_stock)

with db.cursor(pymysql.cursors.Cursor) as cursor:
    sql = """insert into ag_portfolio_history(p_seq, ag_type, id, sub_id, code, stock_name, date, price,
                target_rate, loss_rate, holding_day, reason, percent, type, status) 
            values(105, %s, (select `auto_increment` from INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ag_portfolio_history'), 
                0, %s, %s, %s, %s, 15, -10, 15, '신규편입', 10, 'B', 'H')"""

    args = today_stock

    cursor.execute(sql, args)
    db.commit()

db.close()

