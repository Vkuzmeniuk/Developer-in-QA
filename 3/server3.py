import socket, time, uuid, logging
from multiprocessing import Process,Manager

host = socket.gethostbyname(socket.gethostname())
ports = [8000,8001]
clients = []

def server(server, UNID):
    logging.basicConfig(filename="Logging.log", level=logging.INFO)
    def itsatime():
        itstime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        return itstime
    quit = False
    print(f"[ Server Started]")
    while not quit:
        data, addr = server.recvfrom(1024)
        try:
            print(f"Used {server.getsockname()[1]} port")
            if addr not in clients:
                clients.append(addr)
            if server.getsockname()[1] == 8000:
                message = "Please enter unique identificator: "
                server.sendto(message.encode("utf-8"),addr)
                print(data.decode("utf-8"))
                print(f"[{addr[0]}]=[{addr[1]}]=[{itsatime()}]")
                data, addr = server.recvfrom(1024)
                uid=data.decode("utf-8")
                print(f"Uid = {uid}")
                try:
                    if uid != "":
                        utmp=UNID.get(uid)
                    if bool(utmp) and (addr[1]==utmp[0][1]):
                        server.sendto((f"Your already have unique code: {utmp[1]}").encode("utf-8"),addr)
                        server.sendto(("Switch port").encode("utf-8"),addr)
                    elif not bool(utmp):
                        newid=uuid.uuid4()
                        UNID[uid]=(addr,newid)
                        utmp=UNID.get(uid)
                        print(utmp[1])
                        server.sendto((f"Your unique code: {newid}").encode("utf-8"),addr)
                        server.sendto(("Switch port").encode("utf-8"),addr)
                    break
                except:
                    pass
                
            if server.getsockname()[1] == 8001:
                server.sendto(("Port switched to 8001").encode("utf-8"),addr)
                print(data.decode("utf-8"))
                print(f"[{addr[0]}]=[{addr[1]}]=[{itsatime()}]")
                message = "Enter your message: "
                server.sendto(message.encode("utf-8"),addr)
                data, addr = server.recvfrom(1024)
                umessage = data.decode("utf-8")

                message = "Enter your unique identificator: "
                server.sendto(message.encode("utf-8"),addr)
                data, addr = server.recvfrom(1024)
                uid=data.decode("utf-8")

                message = "Enter your unique code: "
                server.sendto(message.encode("utf-8"),addr)
                data, addr = server.recvfrom(1024)
                ucd=data.decode("utf-8")

                try:
                    uchk=UNID.get(uid)
                    if bool(uchk) and str(uchk[1])==ucd:
                        print("Всё номано!")
                        log_tmp=f"{itsatime()} -- {uid}::{umessage}"
                        logging.info(log_tmp)
                        print(log_tmp)
                    else: 
                        message = "Something went wrong!"
                        server.sendto(message.encode("utf-8"),addr)
                    quit = True
                    break

                except:
                    print("\n[ Server Stopped ]")
                    quit = True         
                
            for client in clients:
                if addr != client:
                    server.sendto(data,client)
        except:	
            print("\n[ Server Stopped ]")
            quit = True
    server.close()

def creating_socket(host,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    return s
    
s1 = creating_socket(host, ports[0])
s2 = creating_socket(host, ports[1])

if __name__ =='__main__':
    manager = Manager()
    UNID = manager.dict()
    p1 = Process(target=server,args=(s1,UNID))
    p2 = Process(target=server,args=(s2,UNID))
    p1.start()
    print(f"Process 1 started")
    p2.start()
    print(f"Process 2 started")
    p1.join()
    p2.join()
    