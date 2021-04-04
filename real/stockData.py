import datetime
from ctypes import *
from struct import pack
from random import randrange

class real_cheg(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("code", c_char * 6),
                ("time", c_char * 6),
                ("price", c_float),
                ("change_price", c_float),
                ("increase_rate", c_float),
                ("sell_1", c_float),
                ("buy_1", c_float),
                ("volume", c_float),
                ("cul_volume", c_float),
                ("cul_amount", c_float),
                ("open", c_float),
                ("high", c_float),
                ("low", c_float),
                ("plus_minus", c_float),
                ("a1", c_float),
                ("a2", c_float),
                ("a3", c_float),
                ("turn_over", c_float),
                ("a4", c_float),
                ("volume_power", c_float),
                ("capitalization", c_float),
                ("market", c_float),
                ("a5", c_float),
                ("high_time", c_float),
                ("low_time", c_float)]

class real_program(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("code", c_char * 6),
                ("time", c_char * 6),
                ("price", c_float),
                ("plus_minus", c_float),
                ("change_price", c_float),
                ("increase_rate", c_float),
                ("cul_volume", c_float),
                ("sell_volume", c_float),
                ("sell_amount", c_float),
                ("buy_volume", c_float),
                ("buy_amount", c_float),
                ("net_buy_volume", c_float),
                ("net_buy_amount", c_float),
                ("a1", c_float),
                ("a2", c_float),
                ("market", c_float),
                ("ticker", c_float)]

def test_cheg_data(codes):
    rand_num = randrange(len(codes))
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
    cheg_hk = real_cheg(index, code, time, price, change_price, increase_rate, sell_1, buy_1,
                                       volume, cul_volume, cul_amount, open, high, low, plus_minus,
                                       a1, a2, a3, turn_over, a4, volume_power, capitalization,
                                       market, a5, high_time, low_time)
    return cheg_hk
    #s.sendto(cheg_hk, ('172.20.10.2', 7777))

def test_program_data(codes):
    rand_num = randrange(len(codes))
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