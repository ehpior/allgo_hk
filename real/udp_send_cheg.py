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
    price = int(randrange(50000))
    change_price = int(randrange(50000))
    increase_rate = int(randrange(50000))
    sell_1 = int(randrange(50000))
    buy_1 = int(randrange(50000))
    volume = int(randrange(50000))
    cul_volume = int(randrange(50000))
    cul_amount = int(randrange(50000))
    open = int(randrange(50000))
    high = int(randrange(50000))
    low = int(randrange(50000))
    plus_minus = 'k'.encode()
    a1 = int(randrange(50000))
    a2 = int(randrange(50000))
    a3 = int(randrange(50000))
    turn_over = int(randrange(50000))
    a4 = int(randrange(50000))
    volume_power = int(randrange(50000))
    capitalization = int(randrange(50000))
    market = int(randrange(50000))
    a5 = int(randrange(50000))
    high_time = int(randrange(50000))
    low_time = int(randrange(50000))

    cheg_hk = stockData_test.real_cheg(index, code, time, price, change_price, increase_rate, sell_1, buy_1,
                                       volume, cul_volume, cul_amount, open, high, low, plus_minus,
                                       a1, a2, a3, turn_over, a4, volume_power, capitalization,
                                       market, a5, high_time, low_time)
    s.sendto(cheg_hk, ('192.168.0.3', 6666))