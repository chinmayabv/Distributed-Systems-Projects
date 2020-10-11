import os
import socket
Buffer_Size = 1024
Server_Directory ="/home/chinmaya/Downloads/Single_and_multi_client_server/Single Server/Server/" 



# Function for uploading file

def upload(filename, link, link_path):
    print "Uploading File" , filename
    file_path = Server_Directory + filename

    with open(file_path, 'wb') as f_write:

        while True:
            data = link.recv(1024)

            if not data:
                break
            f_write.write(data)
        f_write.close()
    print "File Uploaded : ", filename
    link.close()
    return

# Function for downloading file

def download(file_name, link, link_path):
    file_name = Server_Directory + file_name
    if os.path.isfile(file_name):
        link.send("down")

        with open(file_name, 'rb') as f_send:
            data = f_send.read()
            link.send(data)
        print "File downloaded"

    else:
        print "File doesnt exist"
    return

# Function for renaming file

def rename(old_name, new_name, link, link_path):
    old_name = Server_Directory + old_name
    new_name = Server_Directory + new_name

    if not os.path.isfile(old_name):
        print "File not found"
        link.send("File not found")

    else:
        os.rename(old_name, new_name)
        print "File Renamed"
        link.send("File Renamed")
    return

# Function for deleting file

def delete(file_name, link, link_path):
    file_path = Server_Directory + file_name
    if os.path.isfile(file_path):
        os.remove(file_path)
        print "File deleted"
        link.send("File Deleted")

    else:
        print "File doesnt exist"
        link.send("File doesnt exist")
    return




def main():
    HOST = "127.0.0.1"
    PORT = 8080
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind((HOST, PORT))
    s_socket.listen(3)
    print "Server port %s and host %s" % (PORT, HOST)
    print "Connected Server"

    while True:
        print "WAITING FOR CONNECTION FROM CLIENT"
        link, link_path = s_socket.accept()
        link.send("1")
        print "Acknowledgement sent!!"
        input = link.recv(1024)
        msg = input.split(' ')

        if msg[0] == "upload":
            upload(msg[1], link, link_path)

        elif msg[0] == "download":
            download(msg[1], link, link_path)

        elif msg[0] == "rename":
            rename(msg[1], msg[2], link, link_path)

        elif msg[0] == "delete":
            delete(msg[1], link, link_path)

        elif msg[0] == "exit":
            pass
        link.close()
        print "Connection closed"



if __name__ == '__main__':
    main()

