import socket

# Host machine IP
HOST = '127.0.0.1'
# Gazepoint Port
PORT = 4242
ADDRESS = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDRESS)

s.send(str.encode('<SET ID="ENABLE_SEND_CURSOR" STATE="1" />\r\n'))
s.send(str.encode('<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n'))
s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
s.send(str.encode('<SET ID="ENABLE_SEND_COUNTER" STATE="1" />\r\n'))
s.send(str.encode('<SET ID="ENABLE_SEND_TIME" STATE="1" />\r\n'))
s.send(str.encode('<SET ID="ENABLE_SEND_TIME_TICK" STATE="1" />\r\n'))



while 1:
    rxdat = s.recv(1024)
    print(bytes.decode(rxdat))

s.close()