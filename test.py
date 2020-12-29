from socket import *
import numpy as np


class SocketInfo():
    HOST = "192.168.0.3"
    PORT = 8888
    BUFSIZE = 7
    ADDR = (HOST, PORT)

csock = socket(AF_INET, SOCK_STREAM)
csock.connect(SocketInfo.ADDR)
print("conenct is success")

commend = csock.recv(SocketInfo.BUFSIZE, MSG_WAITALL)
data = commend.decode("UTF-8")

print("type : {}, data len : {}, data : {}, Contents : {}".format(type(commend), len(commend), commend, data))
print()

to_server = int(12345)
right_method = to_server.to_bytes(4, byteorder='little')
print("Send Data : {}, bytes len : {}, bytes : {}".format(to_server, len(right_method), right_method))
for i in range(15):
    sent = csock.send(right_method)
    print(sent)

sent = csock.send(int(99999).to_bytes(4, byteorder='little'))

csock.close()
exit()