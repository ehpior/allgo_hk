import datetime
from ctypes import *
from struct import pack
from random import randrange

class real_cheg(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("code", c_char * 6),
                ("time", c_char * 6),
                ("price", c_double),
                ("change_price", c_double),
                ("increase_rate", c_double),
                ("sell_1", c_double),
                ("buy_1", c_double),
                ("volume", c_double),
                ("cul_volume", c_double),
                ("cul_amount", c_double),
                ("open", c_double),
                ("high", c_double),
                ("low", c_double),
                ("plus_minus", c_double),
                ("a1", c_double),
                ("a2", c_double),
                ("a3", c_double),
                ("turn_over", c_double),
                ("a4", c_double),
                ("volume_power", c_double),
                ("capitalization", c_double),
                ("market", c_double),
                ("a5", c_double),
                ("high_time", c_double),
                ("low_time", c_double)]

class real_program(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("code", c_char * 6),
                ("time", c_char * 6),
                ("price", c_double),
                ("plus_minus", c_double),
                ("change_price", c_double),
                ("increase_rate", c_double),
                ("cul_volume", c_double),
                ("sell_volume", c_double),
                ("sell_amount", c_double),
                ("buy_volume", c_double),
                ("buy_amount", c_double),
                ("net_buy_volume", c_double),
                ("net_buy_amount", c_double),
                ("a1", c_double),
                ("a2", c_double),
                ("market", c_double),
                ("ticker", c_double)]

def test_cheg_data(codes):
    print("11")
    print(codes)
    rand_num = randrange(len(codes))
    print("2")
    print(rand_num, end=',')
    print(codes[rand_num])
    print("3")
    index = int(rand_num)
    # code = choice(codes).encode()
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
    print("4")
    cheg_hk = real_cheg(index, code, time, price, change_price, increase_rate, sell_1, buy_1,
                                       volume, cul_volume, cul_amount, open, high, low, plus_minus,
                                       a1, a2, a3, turn_over, a4, volume_power, capitalization,
                                       market, a5, high_time, low_time)
    print("5")
    return cheg_hk
    #s.sendto(cheg_hk, ('172.20.10.2', 7777))

def test_program_data(codes):
    rand_num = randrange(len(codes))

    print(rand_num, end=',')
    print(codes[rand_num])

    index = int(rand_num)
    # code = choice(codes).encode()
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

    cheg_hk = real_program(index, code, time, price, plus_minus, change_price,
                                          increase_rate, cul_volume, sell_volume, sell_amount,
                                          buy_volume, buy_amount, net_buy_volume, net_buy_amount,
                                          a1, a2, market, ticker)

    return cheg_hk
    #s.sendto(cheg_hk, ('172.20.10.2', 8888))