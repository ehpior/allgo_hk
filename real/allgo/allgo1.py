import pymysql, sys


# mysql CRUD : https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

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
#cursor = db.cursor(pymysql.cursors.DictCursor)
#cursor = db.cursor(pymysql.cursors.Cursor)


dates = list()
codes = list()
ds = dict()

with db.cursor(pymysql.cursors.Cursor) as cursor:

    ### 날짜 검사 시작

    sql = """select ifnull(max(date), 0) from ag_score where type='A' and date <= %s"""

    cursor.execute(sql, [today])
    maxDate_score = cursor.fetchone()[0]

    sql = """select ifnull(max(date), 0) from stock_cheg where date <= %s"""

    cursor.execute(sql, [today])
    maxDate_stock = cursor.fetchone()[0]

    print(f"type : A, today : {today}, maxDate_stock : {maxDate_stock}, maxDate_score : {maxDate_score}")

    if (today != maxDate_stock) or (maxDate_stock <= maxDate_score) or (maxDate_stock == 0):
        print("date error")
        exit(1)

    ### 알고리즘 시작

    sql = """SELECT CODE FROM stock_cheg WHERE DATE = %s"""
    args = [today]
    cursor.execute(sql, args)

    for elem in cursor.fetchall():
        codes.append(elem[0])
        ds[elem[0]] = dict()

    sql = """SELECT DATE, a.CODE, round(volume_power, 2) AS 'vp', ROUND((abs(price)-abs(OPEN))/abs(OPEN)*100, 2) AS 'today_increase_rate', 
               round(increase_rate, 2) AS 'increase_rate', abs(OPEN) AS 'open', abs(price) AS 'close', abs(high) AS 'high', abs(low) AS 'low',
               turn_over
            FROM (SELECT CODE FROM stock_cheg WHERE DATE = %s) a
                JOIN stock_cheg b ON b.code = a.code
            WHERE b.DATE > IFNULL((SELECT DISTINCT(DATE)
                    FROM stock_cheg
                    WHERE DATE <= %s
                    ORDER BY DATE desc
                    LIMIT 20, 1), 0)
                AND b.date <= %s
            ORDER BY b.DATE DESC, a.CODE ASC"""

    args = [today, today, today]
    cursor.execute(sql, args)

    for elem in cursor.fetchall():
        tmp_date = elem[0]
        tmp_code = elem[1]
        tmp_vp = elem[2]
        tmp_today_increase_rate = elem[3]
        tmp_increase_rate = elem[4]
        tmp_open = elem[5]
        tmp_close = elem[6]
        tmp_high = elem[7]
        tmp_low = elem[8]
        tmp_turn_over = elem[9]

        if tmp_date not in dates:
            dates.append(tmp_date)

        ds[tmp_code][tmp_date] = {'vp': tmp_vp, 'today_increase_rate': tmp_today_increase_rate,
                        'increase_rate': tmp_increase_rate, 'open': tmp_open, 'close': tmp_close,
                        'high': tmp_high, 'low': tmp_low, 'turn_over': tmp_turn_over}


a = 1
#n = 20  ######################  계산날짜!
n = len(dates)
r = 0.9
discount_value = (1 - r) / (a * (1 - r ** n))

scores = list()

for code in codes:
    days_scores = list()

    for date in dates:
        t_day_score = 0

        if date not in ds[code].keys():
            days_scores = list()
            break

        t_vp = ds[code][date]['vp']
        t_real = ds[code][date]['today_increase_rate']
        t_increase_rate = ds[code][date]['increase_rate']
        t_open = ds[code][date]['open']
        t_close = ds[code][date]['close']
        t_high = ds[code][date]['high']
        t_low = ds[code][date]['low']

        if 0 < t_vp < 20:  ## vp : 체결강도
            t_vp = 20
        elif 180 < t_vp <= 450:
            t_vp = 180

        t_var = (t_vp + 20) / 40

        if t_real < 0:
            t_day_score = (-1 / (22 - 2 * t_var)) * (t_real + 1 - t_var) ** 2 + 1 - 0.5 * t_var
        elif 0 <= t_real < 4:
            t_day_score = (-1 / (9 + t_var)) * (t_real - 3) ** 2 + 1 + abs(-5 + 1.5 * t_var)
        else:
            t_day_score = (-1 / (16 - t_var)) * (t_real - 3) ** 2 + 1 + abs(-5 + 1.5 * t_var)

        if t_vp > 450 or t_vp < 15:
            t_day_score = -10  ## day_score  : 점수

        if t_real >= 0 and t_increase_rate < 0:  ## real : 당일 실등락율 (종가 - 시가)
            t_day_score = t_day_score * 0.5

        if t_high != t_low:
            t_day_score = t_day_score * 0.5 * 1.5 ** abs((t_close - t_open) / (t_high - t_low))
        else:
            t_day_score = t_day_score * 0.5

        days_scores.append(t_day_score)

    if len(days_scores) < n:
        continue

    weighted_sum = 0

    for i, day_score in enumerate(days_scores):

        weighted_value = a * (r ** (i + 1)) * discount_value * day_score
        weighted_sum += weighted_value

    scores.append((code, weighted_sum))

scores = sorted(scores, key=lambda x: x[1], reverse=True)

final_scores = list()

for idx, (code, score) in enumerate(scores):
    # 랭크, 종목코드, 타입, 점수
    final_score = (today, 'A', code, round(score, 2), idx+1)
    final_scores.append(final_score)

print(f"final_scores : {len(final_scores)}")

with db.cursor(pymysql.cursors.Cursor) as cursor:
    sql = "insert into ag_score(date, type, code, score, rank) values(%s, %s, %s, %s, %s)"
    cursor.executemany(sql, final_scores)
    db.commit()

db.close()


