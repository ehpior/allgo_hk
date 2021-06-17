import datetime

import pymysql
import sys

import redis

# mysql CRUD : https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html


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

d = []

with db.cursor(pymysql.cursors.Cursor) as cursor:

    sql = """SELECT ag_type, code, stock_name, average_buy_price, holding_day, first_buy_date
            from ag_portfolio
            where status = 'H'"""

    cursor.execute(sql)

    result = cursor.fetchall()

    if len(result) == 0:
        print("nothing in portfolio")
        exit(1)

    for elem in result:
        tmp_ag_type = elem[0]
        tmp_code = elem[1]
        tmp_stock_name = elem[2]
        tmp_average_buy_price = float(elem[3])
        tmp_holding_day = elem[4]
        tmp_first_buy_date = elem[5]

        d.append({'ag_type': tmp_ag_type, 'code': tmp_code, 'stock_name': tmp_stock_name,
                  'average_buy_price': tmp_average_buy_price,
                  'holding_day': tmp_holding_day, 'first_buy_date': tmp_first_buy_date})


for i, portfolio in enumerate(d):

    ag_type = portfolio['ag_type']
    code = portfolio['code']
    stock_name = portfolio['stock_name']
    average_buy_price = portfolio['average_buy_price']
    holding_day = portfolio['holding_day']
    first_buy_date = portfolio['first_buy_date']

    cur_price = float(abs(float(db_redis.get('stock:' + portfolio['code']))))

    cur_rate = (cur_price - average_buy_price) / average_buy_price * 100

    d[i]['cur_rate'] = cur_rate

    print('------------------')

    print(f'type: {ag_type}, {(stock_name+"("+code+")")}\n buy[{average_buy_price:7.0f}], cur[{cur_price:7.0f}], '
          f'rate[{cur_rate:6.2f}%], max_holding_day[{holding_day}], first_buy_date[{first_buy_date}]')


avg_rate = sum([item['cur_rate'] for item in d]) / len(d)
max_rate = max([item['cur_rate'] for item in d])
min_rate = min([item['cur_rate'] for item in d])

print('\n***********************')
print(f'total_count[{len(d)}], avg_rate[{avg_rate:.2f}%], max_rate[{max_rate:.2f}%], min_rate[{min_rate:.2f}%]')
print('***********************')
db.close()
db_redis.close()

