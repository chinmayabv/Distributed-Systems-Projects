import socket
import pickle

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024

class serial(object):
    pass
    
#Function to perform Addition
def add(num1, num2, con):
    sumval = 0
    con.send("FindSum " + num1 + ' ' + num2)
    return

#Function to get the Sum
def get_sum(con):
    con.send("GetSum" + '')
    sumval = con.recv(BUFFER_SIZE)
    sumval = sumval.split(' ')
    print " sum =", int(sumval[0])

#Function to calculate Pi value
def calculate_pi(con):
    con.send("pi ")
    return

#Function to Get Pi
def get_pi(con):
    con.send("getpi" + '')
    print "Value of pi is:", con.recv(BUFFER_SIZE)
    return

#Function to sort the input array    
def sort(con):
    connectionObj = serial()
    list1 = list()
    n = raw_input("enter the size of array")
    print"Enter the numbers in array"

    for i in range(int(n)):
        x = raw_input("num" + str(i) + ":")
        list1.append(x)
    print "The Unsorted Array: ", list1
    connectionObj.x = list1
    serialized = pickle.dumps(connectionObj)
    con.send("sort " + serialized)
    return

#Function to get the sorted array
def get_sort(con):
    con.send("getsort " + '')
    list1= con.recv(BUFFER_SIZE)
    list2 = pickle.loads(list1)
    print "The sorted Array: ", list2
    return

#Function to multiply 3 matrices
def matrix_multiplication(con):
    matrix1 = list()
    matrix2 = list()
    matrix3 = list()
    print "* Condition for multiplying three matrices \n1. Column of matrix-1 must be equal to Row of matrix-2 \n2.Column of matrix-2 must be equal to Row of matrix-3"
    print"\n Enter size of matix 1 row as n and column as m:"
    n1 = int(input("n1: "))
    m1 = int(input("m1: "))
    print"Enter size of matix 2 row as n and column as m:"
    n2 = int(input("n2: "))
    m2 = int(input("m2: "))
    print"Enter size of matix 3 row as n and column as m:"
    n3 = int(input("n3: "))
    m3 = int(input("m3: "))

    if m1 != n2 & m2 != n3:
        print"Cannot Multiply"
        return
    print "enter matrix 1"
    matrix1 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m1)] for j in range(n1)]
    print "enter matrix 2"
    matrix2 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m2)] for j in range(n2)]
    print "enter matrix 3"
    matrix3 = [[int(raw_input("Enter (%s,%s): " % (i, j))) for i in range(m3)] for j in range(n3)]

    connectionObj = serial()
    connectionObj.x = matrix1
    connectionObj.y = matrix2
    connectionObj.z = matrix3
    serialized = pickle.dumps(connectionObj)
    print "The matrices are:", "\n", matrix1, "\n", matrix2, "\n", matrix3
    con.send("Mat " + serialized)
    return

#Method to receive a Product Matrix    
def get_prod_mat(con):
    con.send("getmat" + '')
    list1 = con.recv(BUFFER_SIZE)
    list2 = pickle.loads(list1)
    print "\nThe result of matrix Multiplication: ","\n", list2
    return

#client method to control the options and operations
def client():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print "Connecting to server %s through port %s" % (HOST,PORT)
    s.connect((HOST,PORT))
    acknowledgement = s.recv(BUFFER_SIZE)

    if acknowledgement == "1":
        print "Connected to server %s and received acknowledgement "%(HOST), acknowledgement
    while True:
        choice = raw_input("Enter your choices from 1 to 9: \n 1.Addition, \n 2.Get Sum, \n 3.Calculate PI, \n 4.Get Pi value, \n 5.Sort Array, \n 6.Get Sorted Array, \n 7.Matrix multiplication, \n 8.Get Product Matrix, \n 9.Exit: ")

        if choice == "1":
            num1 = raw_input("Enter First Number: ")
            num2 = raw_input("Enter Second Number: ")
            add(num1, num2, s)

        elif choice == "2":
            get_sum(s)

        elif choice == "3":
            calculate_pi(s)

        elif choice == "4":
            get_pi(s)

        elif choice == "5":
            sort(s)

        elif choice == "6":
            get_sort(s)

        elif choice == "7":
            matrix_multiplication(s)

        elif choice == "8":
            get_prod_mat(s)

        elif choice == "9":
            s.send("exit ")
            break

        else:
            print "Invalid choices, choose again"
    print "Closing connection..."

    s.close()
    
client()	
