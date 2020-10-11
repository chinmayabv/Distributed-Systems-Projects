import socket
from thread import *
import pickle
import numpy
import math


Buffer_Size = 1024

Data = {'add': 0, 'pi': 0, 'sort': [], 'mat': []}

class serial(object):
    pass

def add(num1, num2):
    s = int(num1) + int(num2)
    Data.update({'add': s})
    print Data['add']
    return


def get_sum(con):
    con.send(str(Data['add']) + ' ')
    

def calculate_pi():
    s = math.pi
    Data.update({'pi': s})
    return


def get_pi(con):
    con.send(str(Data['pi']))
    return

def sort(list1):
    list1 = list1.split(" ", 1)
    list2 = pickle.loads(list1[1])
    list2.x = [int(i) for i in list2.x]
    #print list2.x
    list2.x.sort()
    Data.update({'sort': list2.x})
    #print "Sort is", Data['sort']
    return

def get_sort(con):
    serialize = pickle.dumps(Data['sort'])
    #print serialize
    con.send(serialize)
    return
    
def matrix_multiply(list1):
    list1 = list1.split(" ", 1)
    list2 = pickle.loads(list1[1])
    x = numpy.array(list2.x)
    y= numpy.array(list2.y)
    z = numpy.array(list2.z)
    list2.x = numpy.dot(numpy.dot(x,y),z)
    Data.update({'mat': list2.x})
    #print "matrix is", Data['mat']
    return


def get_prod_mat(con):
    serialize = pickle.dumps(Data['mat'])
    #print serialize
    con.send(serialize)
    return

def thread(con, address):
    while True:
        input = con.recv(Buffer_Size)
        client_message = input.split(' ')

        if client_message[0] == "FindSum":
            add(client_message[1], client_message[2])

        elif client_message[0] == "GetSum":
            get_sum(con)

        elif client_message[0] == "pi":
            calculate_pi()

        elif client_message[0] == "getpi":
            get_pi(con)

        elif client_message[0] == "sort":
            sort(input)

        elif client_message[0] == "getsort":
            get_sort(con)

        elif client_message[0] == "Mat":
            matrix_multiply(input)

        elif client_message[0] == "getmat":
            get_prod_mat(con)

        elif client_message[0] == "exit":
            break

    con.close()
    #print "Connection closed: ", address


def main():
    HOST = "127.0.0.1"
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Starting server on port %s and server %s" % (PORT, HOST)
    s.bind((HOST, PORT))
    s.listen(3)
    try:

        while True:
            link, address = s.accept()
            print "Got connection from ", address
            print "Sending acknowledgment.."
            link.send("1")
            start_new_thread(thread, (link, address,))

    except KeyboardInterrupt:
        pass
    print "\n server closed.."

    s.close()


if __name__ == '__main__':
    main()
