import socket
import json

while True:
    port = 7777
    if str(raw_input('tag or title?  ')) == 'title':
        port = 7778

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port))

    tag = str(raw_input('find word: '))
    if tag == '':
        break
        #send the json request for a socket
    s.send(json.dumps({'query':tag}))
    s.shutdown(socket.SHUT_WR)

    #recieve the response
    try:
        data = bytes()
        while True:
            new_data = s.recv(1024)
            if not new_data: break
            data += new_data
        s.close()
        s = None
        data = str(data)
    except Exception as e:
        print e

    print data
