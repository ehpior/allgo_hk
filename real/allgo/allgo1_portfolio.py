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

    print(f"type : A, today : {today}, maxDate_stock : {maxDate_stock}, maxDate_score : {maxDate_score}")

    if (maxDate_stock != maxDate_score) or (businessDay_state != 3) or (maxDate_stock == 0) or (maxDate_score == 0):
        print("datetime error")
        exit(1)

    ### 알고리즘 시작

    sql = """SELECT a.code, a.score, a.rank
        FROM ag_score a 
            INNER JOIN (SELECT a.code
                FROM stock_cheg a
                WHERE a.DATE >= IFNULL((SELECT DISTINCT(DATE)
                        FROM stock_cheg
                        WHERE DATE < %s
                        ORDER BY DATE desc
                        LIMIT 19, 1), 0)
                    AND a.date < %s
                GROUP BY a.code
                HAVING AVG(a.turn_over) >= 1.5 
                    AND AVG(a.capitalization) >= 2000 
                    AND COUNT(1) = 20) b ON b.code = a.code
            LEFT JOIN ag_portfolio c ON c.code = a.code AND c.`status` = 'H'
        WHERE a.date = (SELECT MAX(DATE) FROM ag_score WHERE DATE < %s)
            AND a.type = 'A'
            AND a.score >= 0.7
            AND c.code IS null
        ORDER BY a.RANK asc"""

    args = [today, today, today]
    cursor.execute(sql, args)

    result = cursor.fetchall()

    if len(result) == 0:
        print("nothing")
        exit(1)

    d_today['code'] = str(result[0][0])

d_today['price'] = float(db_redis.get('stock:' + d_today['code']))


today_stock = (today, 'A', d_today['code'], abs(d_today['price']))

print(today_stock)


#with db.cursor(pymysql.cursors.Cursor) as cursor:
#    sql = "insert into ag_score(date, type, code, score, rank) values(%s, %s, %s, %s, %s)"
#    cursor.executemany(sql, final_scores)
#    db.commit()
#
#db.close()


