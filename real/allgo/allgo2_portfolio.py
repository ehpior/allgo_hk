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

#today = sys.argv[1]
today = '20210521'
if len(today) != 8:
    print('len(today) error')
    exit(1)

dates = list()
codes = list()
ds = dict()

sql = """SELECT a.CODE 
    FROM stock_program a
        INNER JOIN stock_cheg b ON b.date = a.date AND b.code = a.code AND b.capitalization >= 3000
    WHERE a.date = %s"""
args = [today]
cursor.execute(sql, args)

for elem in cursor.fetchall():
    codes.append(elem[0])
    ds[elem[0]] = list()


sql = """SELECT a.date, a.CODE, round(a.net_buy_amount / b.capitalization * 100, 2) AS 'score'
    FROM (SELECT a.CODE 
            FROM stock_program a
                INNER JOIN stock_cheg b ON b.date = a.date AND b.code = a.code AND b.capitalization >= 3000
            WHERE a.date = %s) f
        INNER JOIN stock_program a ON a.code = f.code
        INNER JOIN stock_cheg b ON b.date = a.date AND b.code = f.code
    WHERE a.DATE > IFNULL((SELECT DISTINCT(DATE)
            FROM stock_program
            WHERE DATE <= %s
            ORDER BY DATE desc
            LIMIT 20, 1), 0)
        AND a.date <= %s
    ORDER BY a.date DESC, a.code asc"""
args = [today, today, today]
cursor.execute(sql, args)


for elem in cursor.fetchall():
    tmp_date = elem[0]
    tmp_code = elem[1]
    tmp_score = elem[2]

    dates.append(tmp_date)
    ds[tmp_code].append(tmp_score)

final_score = list()

for code in codes:
    days_scores = list()

    if max(ds[code][0:-1]) <= ds[code][-1]:
        pass
    else:
        continue




sql = "insert into ag_score(date, type, code, score) values(%s, %s, %s, %s)"
cursor.executemany(sql, final_score)
db.commit()


