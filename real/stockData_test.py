import datetime
from ctypes import *
from struct import pack

class real_program(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("code", c_char * 6),
                ("time", c_char * 6),
                ("price", c_uint32),
                ("plus_minus", c_char),
                ("change_price", c_uint32),
                ("increase_rate", c_uint32),
                ("cul_volume", c_uint32),
                ("sell_volume", c_uint32),
                ("sell_amount", c_uint32),
                ("buy_volume", c_uint32),
                ("buy_amount", c_uint32),
                ("net_buy_volume", c_uint32),
                ("net_buy_amount", c_uint32),
                ("a1", c_uint32),
                ("a2", c_uint32),
                ("market", c_uint32),
                ("ticker", c_uint32)]

class real_cheg(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("code", c_char * 6),
                ("time", c_char * 6),
                ("price", c_uint32),
                ("change_price", c_uint32),
                ("increase_rate", c_uint32),
                ("sell_1", c_uint32),
                ("buy_1", c_uint32),
                ("volume", c_uint32),
                ("cul_volume", c_uint32),
                ("cul_amount", c_uint32),
                ("open", c_uint32),
                ("high", c_uint32),
                ("low", c_uint32),
                ("plus_minus", c_char),
                ("a1", c_uint32),
                ("a2", c_uint32),
                ("a3", c_uint32),
                ("turn_over", c_uint32),
                ("a4", c_uint32),
                ("volume_power", c_uint32),
                ("capitalization", c_uint32),
                ("market", c_uint32),
                ("a5", c_uint32),
                ("high_time", c_uint32),
                ("low_time", c_uint32)]

