import socket
from thread import *
import pickle
import numpy
import math

Buffer_Size = 1024


class serial(object):
    pass


#Function to add 2 numbers
def add(con, num1, num2):
    print "Adding 2 numbers"
    sum = int(num1) + int(num2)
    con.send(str(sum) + ' ')
    return


#Function to calculate Pi value
def calculate_pi(con):
    print "Server Calculating Pi"
    result = math.pi
    con.send(str(result))
    return

#Function to sort the input array
def sort(con, arr):
    print "Sorting an Array"
    arr = arr.split(" ", 1)
    res = pickle.loads(arr[1])
    res.x = [int(i) for i in res.x]
    res.x.sort()
    x = pickle.dumps(res)
    con.send(x)
    return


#Function to multiply 3 matrices
def matrix_multiply(con, A):
    print "Multiplying 3 matrices"
    A = A.split(" ", 1)
    B = pickle.loads(A[1])
    x = numpy.array(B.x)
    y = numpy.array(B.y)
    z = numpy.array(B.z)
    B.x = numpy.dot(numpy.dot(x, y), z)
    serialized = pickle.dumps(B)
    con.send(serialized)
    return

#Creating a thread for the received connection
def thread(con, address):
    while True:
        input = con.recv(Buffer_Size)
        Client_message = input.split(' ')

        if Client_message[0] == "FindSum":
            add(con, Client_message[1], Client_message[2])

        elif Client_message[0] == "pi":
            calculate_pi(con)

        elif Client_message[0] == "sort":
            sort(con, input)

        elif Client_message[0] == "Mat":
            matrix_multiply(con, input)

        elif Client_message[0] == "exit":
            break


    con.close()
    print "Connection closed: ", address


def main():
    HOST = "127.0.0.1"
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Starting server on port %s and server %s" % (PORT, HOST)
    s.bind((HOST, PORT))
    s.listen(3)
    try:
        while True:
            print "Waiting for Connection..."
            con, address = s.accept()
            print "Got Connected to ", address
            print "Sending acknowledgment.."
            con.send("1")
            start_new_thread(thread, (con, address,))
    except KeyboardInterrupt:
        pass
    print "\n server closed.."
    s.close()


if __name__ == '__main__':
    main()
