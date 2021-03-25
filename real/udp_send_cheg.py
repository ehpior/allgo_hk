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
    change_price = float(randrange(50000))
    increase_rate = float(randrange(50000))
    sell_1 = float(randrange(50000))
    buy_1 = float(randrange(50000))
    volume = float(randrange(50000))
    cul_volume = float(randrange(50000))
    cul_amount = float(randrange(50000))
    open = float(randrange(50000))
    high = float(randrange(50000))
    low = float(randrange(50000))
    plus_minus = float(randrange(50000))
    a1 = float(randrange(50000))
    a2 = float(randrange(50000))
    a3 = float(randrange(50000))
    turn_over = float(randrange(50000))
    a4 = float(randrange(50000))
    volume_power = float(randrange(50000))
    capitalization = float(randrange(50000))
    market = float(randrange(50000))
    a5 = float(randrange(50000))
    high_time = float(randrange(50000))
    low_time = float(randrange(50000))

    cheg_hk = stockData_test.real_cheg(index, code, time, price, change_price, increase_rate, sell_1, buy_1,
                                       volume, cul_volume, cul_amount, open, high, low, plus_minus,
                                       a1, a2, a3, turn_over, a4, volume_power, capitalization,
                                       market, a5, high_time, low_time)
    s.sendto(cheg_hk, ('172.20.10.2', 7777))