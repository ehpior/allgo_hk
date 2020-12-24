from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

종목상태 = kiwoom.GetMasterStockState("020560")
print(종목상태)