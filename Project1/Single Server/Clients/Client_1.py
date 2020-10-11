import os
import socket

HOST = "127.0.0.1"
PORT = 8080
Buffer_Size = 1024

Client_Directory = "/home/chinmaya/Downloads/Single_and_multi_client_server/Single Server/Clients/" 



def get_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print "Connecting to Server"
    ack = sock.recv(Buffer_Size)
    if ack == "1":
        print "Acknowledgement Received"
        return sock


def upload(file_name, socket_path):
    socket_path.send("upload " + file_name)
    file_path = Client_Directory + file_name

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f_send:
            data = f_send.read()
            socket_path.send(data)
        socket_path.close()

        print "File Uploaded" 

    else:
        print "File doesnt exist"

    socket_path.close()
    return


# Function for downloading file

def download(file_name, socket_path):
    socket_path.send("download " + file_name)
    message = socket_path.recv(Buffer_Size)
    file_path = Client_Directory + file_name

    if message == "down":

        with open(file_path, 'wb') as f_write:

            while True:
                data = socket_path.recv(Buffer_Size)

                if not data:
                    break
                f_write.write(data)
            f_write.close()
        print "File Downloaded"

    else:
        print "File not found"

    socket_path.close()
    return


# Function for renaming file

def rename(old_name, new_name, socket_path):
    socket_path.send("rename " + old_name + " " + new_name)
    message = socket_path.recv(Buffer_Size)
    print message
    socket_path.close()
    return

# Function for deleting file


def delete(file_name, socket_path):
    socket_path.send("delete " + file_name)
    message = socket_path.recv(Buffer_Size)
    print message
    socket_path.close()
    return


# Main function for Client to operate

def client_option():
    while True:
        socket_path = get_socket()
        opt = raw_input("Choose operation: \n 1.upload, \n 2.download, \n 3.rename, \n 4.delete, \n 5.exit: ")

        if opt == "1":
            file_name = raw_input("File name to upload: ")
            upload(file_name, socket_path)

        elif opt == "2":
            file_name = raw_input("File name to download: ")
            download(file_name, socket_path)

        elif opt == "3":
            old_name = raw_input("Old name of File: ")
            new_name = raw_input("New name of File: ")
            rename(old_name, new_name, socket_path)

        elif opt == "4":
            file_name = raw_input("File name to delete: ")
            delete(file_name, socket_path)

        elif opt == "5":
            socket_path.send("exit ")
            break

        else:
            print "Invalid choices, choose again"

    socket_path.close()


client_option()
