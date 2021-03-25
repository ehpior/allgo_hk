import stockData_test, socket
import sys
from random import choice, randrange


codes = []
with open('codes.txt', 'r') as f:
    codes = f.readline()
    codes = codes.split(';')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(10):
    rand_num = randrange(len(codes))

    print(rand_num, end=',')
    print(codes[rand_num])

    index = int(rand_num)
    #code = choice(codes).encode()
    code = codes[rand_num].encode()
    time = '210312'.encode()
    price = float(randrange(50000))
    plus_minus = float(randrange(50000))
    change_price = float(randrange(50000))
    increase_rate = float(randrange(50000))
    cul_volume = float(randrange(50000))
    sell_volume = float(randrange(50000))
    sell_amount = float(randrange(50000))
    buy_volume = float(randrange(50000))
    buy_amount = float(randrange(50000))
    net_buy_volume = float(randrange(50000))
    net_buy_amount = float(randrange(50000))
    a1 = float(randrange(50000))
    a2 = float(randrange(50000))
    market = float(randrange(50000))
    ticker = float(randrange(50000))

    cheg_hk = stockData_test.real_program(index, code, time, price, plus_minus, change_price,
                                       increase_rate, cul_volume, sell_volume, sell_amount,
                                       buy_volume, buy_amount, net_buy_volume, net_buy_amount,
                                       a1, a2, market, ticker)

    s.sendto(cheg_hk, ('172.20.10.2', 8888))