import socket, threading, time, queue

shutdown = False
join1 = False
join2 = False
def receving (name, sock, thread_return):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				print(data.decode("utf-8"))
				time.sleep(0.2)
				if data.decode("utf-8")=="Switch port":
					print("Server send command switch port ")
					thread_return['switch_port']=True
					break
		except:
			pass
host = socket.gethostbyname(socket.gethostname())
port = 0

server1 = (socket.gethostname(),8000)
server2 = (socket.gethostname(),8001)


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(False)
thread_return={'switch_port':False}

while shutdown == False:
	if join1 == False:
		alias = input("Name: ")
		rT = threading.Thread(target = receving, args = ("RecvThread",s,thread_return))
		rT.start()
		s.sendto((f"[{alias}] => join").encode("utf-8"),server1)
		join1 = True
	elif thread_return.get('switch_port') and join2 == False:
		alias = input("Name: ")
		s.sendto((f"[{alias}] => join").encode("utf-8"),server2)
		
		join2 = True
	else:
		try:
			message = input("")
			if message != "" and not thread_return.get('switch_port'):
				messageto = f"{message}"
				s.sendto(messageto.encode("utf-8") ,server1)

			elif message != "" and thread_return.get('switch_port'):
				messageto = f"{message}"
				s.sendto(messageto.encode("utf-8") ,server2)
			time.sleep(0.2)
		except:
			s.sendto((f"[{alias}] <= left ").encode("utf-8"),server1)
			s.sendto((f"[{alias}] <= left ").encode("utf-8"),server2)
			shutdown = True

rT.join()
s.close()