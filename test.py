import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 7777))
			

	#send the json request for a socket
s.send(json.dumps({"request_type":"tag_search",'tag':'disney'}))
s.shutdown(socket.SHUT_WR)

#recieve the response
try:
    data = bytes()
    while True:
        new_data = s.recv(1024)
        if not new_data: break
        data += new_data
    s.close()
    data = str(data)
except Exception as e:
    print e

print data
