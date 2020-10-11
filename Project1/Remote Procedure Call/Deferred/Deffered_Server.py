import socket
from decimal import Decimal, getcontext
from thread import *
import threading
import pickle
import numpy

lock = threading.Lock()
BUFFER_SIZE = 1024

class serial(object):
    pass

def add(con, address, num1, num2):  
    #print connection
    sum1 = int(num1) + int(num2)
    con.send(str(sum1) + ' ')
    return

def calculate_pi(con):  
    getcontext().prec = 100
    s = sum(1 / Decimal(16) ** i * (
                Decimal(4) / (8 * i + 1) - Decimal(2) / (8 * i + 4) - Decimal(1) / (8 * i + 5) - Decimal(1) / (
                    8 * i + 6)) for i in range(1000))
    con.send(str(s))
    return

def sort(con, list1):
    list1 = list1.split(" ", 1)
    list2 = pickle.loads(list1[1])
    list2.x = [int(i) for i in list2.x]
    list2.x.sort()
    x = pickle.dumps(list2)
    con.send(x)
    return


def matrix_multiplication(con, list1):
    list1 = list1.split(" ", 1)
    list2 = pickle.loads(list1[1])
    x = numpy.array(list2.x)
    y = numpy.array(list2.y)
    z = numpy.array(list2.z)
    list2.x = numpy.dot(numpy.dot(x, y), z)
    serialized = pickle.dumps(list2)
    con.send(serialized)
    return
    
    
def threaded(con, address):
    while True:
        commands = con.recv(BUFFER_SIZE)
        input_values = commands.split(' ')

        if input_values[0] == "FindSum":
            lock.acquire()
            add(con, address, input_values[1], input_values[2])
            lock.release()

        elif input_values[0] == "calculate_pi":
            lock.acquire()
            calculate_pi(con)
            lock.release()

        elif input_values[0] == "sort":
            lock.acquire()
            sort(con, commands)
            lock.release()

        elif input_values[0] == "mat":
            lock.acquire()
            matrix_multiplication(con, commands)
            lock.release()

        elif input_values[0] == "exit":
            break


    con.close()
    print "Connection closed: ", address

def main():
    HOST = "127.0.0.1"
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Starting server on port %s and server %s" % (PORT, HOST)
    s.bind((HOST, PORT))
    s.listen(5)

    try:

        while True:
            print "waiting for connection..press control+c  to exit server"
            con, address = s.accept()
            print "Got connection from ", address
            print "Sending acknowledgment.."
            con.send("ACK")
            start_new_thread(threaded, (con, address,))
    except KeyboardInterrupt:
        pass
    print "\n server closed.."
    s.close()


if __name__ == '__main__':
    main()
