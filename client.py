import socket
import time
import select
import sys
s = socket.socket()
print("Enter IP address of server")
host = input()
print("Enter port")
port = input()

s.connect((host, int(port))) # Connect to server

# Receive questions and answer
inst=str(s.recv(1024),"utf-8")
print (inst)
p=int(inst[20:22])
k=0
a=str(s.recv(1024),"utf-8")
print(a)
y=str(s.recv(1024),"utf-8")
print(y)
while (k<=p):
     
    data = str(s.recv(1024),"utf-8")
    if data=="Hi":
        break
    print(data)
    c,c1,c2=select.select([sys.stdin,s],[],[],20)
    if len(c)>0:
        if c[0] == sys.stdin:
            y=input()
            s.send(str.encode(y))
        else:
            d=str(c[0].recv(1024),"utf-8")
            print (d)
            k=k+1
            continue;
    data2=str(s.recv(1024),"utf-8")
    print (data2)
    if data2=='Answer the Question':
        ans=input()
        time.sleep(1)
        s.send(str.encode(ans))
        k=k+1
        
        
        rep=str(s.recv(1024),"utf-8")
        print(rep)
        
    
data3=str(s.recv(1024),"utf-8")
print(data3)





    
