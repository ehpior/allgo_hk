import pymysql


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

today = '20210517'

dates = list()
codes = list()
ds = dict()

sql = """SELECT CODE FROM stock_cheg WHERE DATE = %s"""
args = [today]
cursor.execute(sql, args)

for elem in cursor.fetchall():
    codes.append(elem[0])
    ds[elem[0]] = dict()


sql = """SELECT DATE, a.CODE, round(volume_power, 2) AS 'vp', ROUND((abs(price)-abs(OPEN))/abs(OPEN)*100, 2) AS 'today_increase_rate', 
           round(increase_rate, 2) AS 'increase_rate', abs(OPEN) AS 'open', abs(price) AS 'close', abs(high) AS 'high', abs(low) AS 'low'
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

    dates.append(tmp_date)
    ds[tmp_code][tmp_date] = {'vp': tmp_vp, 'today_increase_rate': tmp_today_increase_rate,
                    'increase_rate': tmp_increase_rate, 'open': tmp_open, 'close': tmp_close,
                    'high': tmp_high, 'low': tmp_low}

a = 1
#n = 20  ######################  계산날짜!
n = len(dates)
r = 0.9
discount_value = (1 - r) / (a * (1 - r ** n))

final_score = list()

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

    print(f'final[{code}] : {weighted_sum}')

    final_score.append([today, 'Z', code, round(weighted_sum, 2)])


sql = "insert into ag_score(date, type, code, score) values(%s, %s, %s, %s)"
cursor.executemany(sql, final_score)
db.commit()


