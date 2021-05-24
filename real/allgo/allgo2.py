import pymysql, sys


# mysql CRUD : https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

db = pymysql.connect(
    user='jhk',
    passwd='wjdgusrl34',
    host='1.240.167.231',#'10.211.55.2',
    db='allgo',
    charset='utf8'
)
#cursor = db.cursor(pymysql.cursors.DictCursor)
cursor = db.cursor(pymysql.cursors.Cursor)

today = sys.argv[1]
#today = '20210521'
if len(today) != 8:
    print('len(today) error')
    exit(1)

sql = """insert into ag_score(date, type, code, score)
    SELECT a.date, 'B', a.CODE, round(a.net_buy_amount / b.capitalization * 100, 2) AS 'score'
    FROM stock_program a
        INNER JOIN stock_cheg b ON b.date = a.date AND b.code = a.code
    WHERE a.date = %s"""
args = [today]
cursor.execute(sql, args)

db.commit()


