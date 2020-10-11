import socket
import pickle

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024

class serial(object):
    pass

#Function to add 2 numbers
def add(num1,num2,con):
    totalSum = 0
    con.send("FindSum " + num1 + ' ' + num2)
    totalSum = con.recv(BUFFER_SIZE)
    totalSum = totalSum.split(' ')
    print "Sum =", int(totalSum[0])
    return

#Function to calculate Pi value
def calculate_pi(con):
    con.send("pi ")
    print(con.recv(BUFFER_SIZE))
    return

#Function to sort the input array
def sort(con):
    connectionObj =  serial()
    list1 = list()
    num = raw_input("Enter the size of Array")
    print "Enter the number in Array"
    for i in range(int(num)):
        x = raw_input("Number "+str(i)+" :")
        list1.append(x)
    print "Unsorted Array: ",list1
    connectionObj.x = list1
    serialized = pickle.dumps(connectionObj)
    con.send("sort " + serialized)
    s = pickle.loads(con.recv(BUFFER_SIZE))
    return (s.x)
    # connectionObj.x = list1
    # serialized = pickle.dumps(connectionObj)
    # con.send("sort " + serialized)
    # sortedarr = pickle.loads(con.recv(BUFFER_SIZE))
    # return (sortedarr.x)

#Function to multiply 3 matrices
def matrix_multiply(con):
    matrix1 = list()
    matrix2 = list()
    matrix3 = list()
    print "Multiplication of Matrices conditions: \n 1.Column of matrix-1 must be equal to Row of matrix-2\n2.1.Column of matrix-2 must be equal to Row of matrix-3"
    print "Enter the size of Matrix-1"
    n1 = int(input("n1: "))
    m1 = int(input("n1: "))
    print "Enter the size of Matrix-2"
    n2 = int(input("n2: "))
    m2 = int(input("n2: "))
    print "Enter the size of Matrix-3"
    n3 = int(input("n3: "))
    m3 = int(input("n3: "))
    if m1!=n2 or m2!=n3:
        print "Cannot Multiply"
        return
    print "Enter values to Matrix-1"
    matrix1 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m1)] for j in range(n1)]
    print "Enter values to Matrix 2"
    matrix2 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m2)] for j in range(n2)]
    print "Enter values to Matrix 3"
    matrix3 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m3)] for j in range(n3)]

    connectionObj = serial()
    connectionObj.x = matrix1
    connectionObj.y = matrix2
    connectionObj.z = matrix3
    serialized = pickle.dumps(connectionObj)
    con.send("Mat "+serialized)
    result = pickle.loads(con.recv(BUFFER_SIZE))
    return (result.x)


#client method to control the options and operations
def client():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print "Connecting to server %s through port %s" % (HOST,PORT)
    s.connect((HOST,PORT))
    acknowledgement = s.recv(BUFFER_SIZE)

    if acknowledgement == "1":
        print "Connected to server %s and received acknowledgement "%(HOST), acknowledgement

    while True:
        choice = raw_input("Enter your choice from 1 to 5\n 1.Addition\n 2.Calculate PI\n 3.Sort \n 4.Matrix Multiplication\n 5.Exit\n")
        if choice == "1":
            num1 = raw_input("Enter First Number: ")
            num2 = raw_input("Enter Second Number: ")
            add(num1, num2, s)
        elif choice == "2":
            calculate_pi(s)
        elif choice == "3":
            arr = sort(s)
            print "The sorted Array: ",arr
        elif choice == "4":
            product = matrix_multiply(s)
            print "The Product Matrix is: \n", product
        elif choice == "5":
            s.send("exit ")
            break
        else:
            print "Invalid choices, choose again"
    print "Connection Closing.."
    s.close()

#Calling the Client method
client()
