import socket
import sys
import time
import select

all_connections = []
all_address = []
Questions=["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10"]
Answers=[1,2,3,4,5,6,7,8,9,10]
Marks=[0,0,0]
response=[]


# Create a Socket ( for connecting two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host ="" 
        print("Enter Port") 
        port = input()
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, int(port)))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")


# Handling connection from multiple playes and saving to a list
# Closing previous connections when server.py file is restarted
#send instructions to players and start game
def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]
    j=0
    while True:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout
            j=j+1
            all_connections.append(conn)
            all_address.append(address)
            if j<3:
                print("Connection has been established :Client " + str(j)+" " + address[0])
                conn.send(str.encode("Total questions are 10. First one to reach 4 points wins.First enter yes for buzzer and then answer the question.If you don't know the question just don't press buzzer"))
                time.sleep(1)
                conn.send(str.encode("You are Player : "+ str(j)))
                time.sleep(1)
                conn.send(str.encode("Welcome the game"))

            else:
                print("Connection has been established :Client " + str(j)+" " + address[0])
                conn.send(str.encode("Total questions are 10. First one to reach 4 points wins.First enter yes for buzzer and then answer the question.If you don't know the question just don't press buzzer"))
                print("Maximum Clients connected")
                time.sleep(1)
                conn.send(str.encode("You are Player : "+ str(j)))
                time.sleep(1)
                conn.send(str.encode("Welcome to the game"))



                thread_function()
                break;
# Function for handling Marks and questions                
def thread_function():
    
    for i in range(len(Questions)):
        for conn in all_connections:
            time.sleep(0.1)
            conn.send(str.encode(Questions[i]+": Do You Know this question?"))
        response1=select.select(all_connections,[],[],20)#str(conn.recv(1024),"utf-8")
        if(len(response1[0])>0):
            
            conn_name = response1[0][0];
            b = conn_name.recv(1024)
            b = b.decode("utf-8")
            response1=()
            for conn in all_connections:
                if conn!=conn_name:
                    conn.send(str.encode("Sorry, Player "+str(all_connections.index(conn_name)+1)+ " has pressed the buzzer."))
            for p in range(len(all_connections)):
                    if all_connections[p]==conn_name:
                        t=p;

            if b=='Yes' or b=='yes' or b=='YES' or b=='y':
                        conn_name.send(str.encode("Answer the Question"))
                        answer=str(conn_name.recv(1024),"utf-8")
                        if answer==str(Answers[i]):
                            
                            Marks[t]=Marks[t]+1
                            conn_name.send(str.encode("Correct Answer, You get 1 Point"))
                            if Marks[t]==4:
                                   
                                for c in all_connections:
                                    c.send(str.encode("Hi"))
                                    time.sleep(1)

                                
                                break
                        else:
                            conn_name.send(str.encode("Wrong Answer, You get 0 Points"))
                            time.sleep(1)
            elif b==str(Answers[i]):
                conn_name.send(str.encode("You didn't press the buzzer before answering.You get -1 points"))
                Marks[t]=Marks[t]-1
                time.sleep(1)


        else:
            for c in all_connections:
                c.send(str.encode("Nobody pressed the buzzer.Moving on to the next question"))
# Start program and declare winner.
def main():
    create_socket()
    bind_socket()
    accepting_connections()
    y=0
    d=0
    for i in range(len(all_connections)):
        if Marks[i]>y:
            d=i
            y=Marks[i]
    for c in all_connections:
        if all_connections.index(c)!=d:
            c.send(str.encode("The winner is Player: " + str(d+1)+" with "+str(y)+" Points" ))
        else:
            c.send(str.encode("Congratulations! You are the winner with " + str(y)+" Points" ))
        


main()
