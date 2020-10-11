import socket
import pickle
from threading import Thread
import time


HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024

class serial(object):
    pass

#Function to add 2 numbers
def add(num1,num2,con):
    sum = 0
    con.send("FindSum " + num1 + ' ' + num2)
    s = con.recv(BUFFER_SIZE)
    s = s.split(' ')
    print " sum =", int(s[0])
    return
   
#Function to calculate Pi value
def calculate_pi(con):
    con.send("calculate_pi ")
    print(con.recv(BUFFER_SIZE))
    return

#Function to sort the input array
def sort(con):
    connectionObj = serial()
    list1 = list()
    n = raw_input("enter the size of array")
    print"enter the numbers in array"
    for i in range(int(n)):
        x = raw_input("num" + str(i) + ":")
        list1.append(x)
   # print A
    connectionObj.x = list1
    serialized = pickle.dumps(connectionObj)
    con.send("sort " + serialized)
    result = pickle.loads(con.recv(BUFFER_SIZE))
    return (result.x)

#Function to multiply 3 matrices
def matrix_multiply(con):
    matrix1 = list()
    matrix2 = list()
    matrix3 = list()
    print"enter size of matix 1"
    n1 = int(input("n1: "))
    m1 = int(input("m1: "))
    print"enter size of matix 2"
    n2 = int(input("n2: "))
    m2 = int(input("m2: "))
    print"enter size of matix 3"
    n3 = int(input("n3: "))
    m3 = int(input("m3: "))

    if m1 != n2 & m2 != n3:
        print"Cannot Multiply"
        return
    print "Enter Matrix 1"
    matrix1 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m1)] for j in range(n1)]
    print "Enter Matrix 2"
    matrix2 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m2)] for j in range(n2)]
    print "Enter Matrix 3"
    matrix3 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m3)] for j in range(n3)]

    connectionObj = serial()
    connectionObj.x = matrix1
    connectionObj.y = matrix2
    connectionObj.z = matrix3
    serialized = pickle.dumps(connectionObj)
    print matrix1, matrix2, matrix3
    con.send("mat " + serialized)
    s = pickle.loads(con.recv(BUFFER_SIZE))
    return (s.x)
  
#client method to control the options and operations  
def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to port %s and server %s  " % (PORT, HOST)
    s.connect((HOST, PORT))
    acknowledgement = s.recv(BUFFER_SIZE)

    if acknowledgement == "ACK":
        print "Connected to server and got acknowledgments: ", acknowledgement

    while True:
        choice = raw_input("Enter your choice from 1 to 5\n 1.Addition\n 2.Calculate PI\n 3.Sort \n 4.Matrix Multiplication\n 5.Exit\n")
        if choice == "1":
            num1 = raw_input("Enter number1  ")
            num2 = raw_input("Enter number2  ")
            add(num1, num2, s)

        elif choice == "2":
            calculate_pi(s)

        elif choice == "3":
            list1 = sort(s)
            print list1

        elif choice == "4":
            list2 = matrix_multiply(s)
            print list2

        elif choice == "5":
            s.send("exit ")
            break

        else:
            print "Invalid choices, choose again"
    print "Closing connection..."

    s.close()

client()
