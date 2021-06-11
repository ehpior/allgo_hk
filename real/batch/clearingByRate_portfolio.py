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

businessDay_state = db_redis.get('businessDay_state')

d = []
dates = [today]

with db.cursor(pymysql.cursors.Cursor) as cursor:

    ### 날짜 검사 시작
    print(f"type : clearingByRate_portfolio, today : {today}")

    if businessDay_state != '3':
        print("datetime error")
        exit(1)

    ### 알고리즘 시작

    sql = """select id, p_seq, code, holding_day, stock_name, average_buy_price, first_buy_date
        from ag_portfolio
        where status = 'H'"""

    cursor.execute(sql)

    result = cursor.fetchall()

    if len(result) == 0:
        print("nothing on portfolio")
        exit(1)

    for elem in result:
        tmp_id = elem[0]
        tmp_p_seq = elem[1]
        tmp_code = elem[2]
        tmp_holding_day = elem[3]
        tmp_stock_name = elem[4]
        tmp_average_buy_price = float(elem[5])
        tmp_first_buy_date = elem[6]

        d.append({'id': tmp_id, 'p_seq': tmp_p_seq, 'code': tmp_code, 'holding_day': tmp_holding_day,
                  'stock_name': tmp_stock_name, 'avg_buy_price': tmp_average_buy_price,
                  'first_buy_date': tmp_first_buy_date})

final_data = []
target_rate = 1.15
loss_rate = 0.90

for i, portfolio in enumerate(d):

    cur_price = float(abs(float(db_redis.get('stock:' + portfolio['code']))))

    target_price = portfolio['avg_buy_price'] * target_rate
    loss_price = portfolio['avg_buy_price'] * loss_rate

    if cur_price >= target_price:
        final_data.append((portfolio['id'], portfolio['id'], portfolio['code'], portfolio['stock_name'],
                           today, cur_price, '목표가도달'))
        print(f'[id: {portfolio["id"]}, {portfolio["stock_name"]}({portfolio["code"]}), '
              f'avg_buy_price: {round(portfolio["avg_buy_price"])}, '
              f'cur_price: {round(cur_price)}, rate: {round((cur_price/portfolio["avg_buy_price"]-1)*100, 2)}, '
              f'reason: 목표가도달]')

    elif cur_price < loss_price:
        final_data.append((portfolio['id'], portfolio['id'], portfolio['code'], portfolio['stock_name'],
                           today, cur_price, '손절가도달'))
        print(f'[id: {portfolio["id"]}, {portfolio["stock_name"]}({portfolio["code"]}), '
              f'avg_buy_price: {round(portfolio["avg_buy_price"])}, '
              f'cur_price: {round(cur_price)}, rate: {round((cur_price/portfolio["avg_buy_price"]-1)*100, 2)}, '
              f'reason: 손절가도달]')

if len(final_data) == 0:
    #print('nothing to clear')
    exit(0)

with db.cursor(pymysql.cursors.Cursor) as cursor:
    sql = """insert into ag_portfolio_history(p_seq, id, sub_id, code, stock_name, date, price,
                reason, percent, type, status)
            values(105, %s, (select max(sub_id) + 1 from ag_portfolio_history as a where id = %s),
                %s, %s, %s, %s, %s, 10, 'S', 'S')"""

    cursor.executemany(sql, final_data)
    db.commit()

db.close()
db_redis.close()

