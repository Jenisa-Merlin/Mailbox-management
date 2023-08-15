import socket
import os

PORT = 3777
HOST = '10.1.66.155'
FORMAT = 'utf-8'
SIZE = 1024

username = ''
user_email = ''

def get_user_name():
    return os.path.splitext(os.path.basename(__file__))[0]

def connect_to_server():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        return s

def send_data_to_server(data,s):
    str_data = '|'.join(data)
    s.send(str_data.encode(FORMAT))

def get_data_from_server(s):
    server_data = s.recv(SIZE).decode(FORMAT)
    s.close()
    return server_data

def get_data_from_server_splitted(s):
    server_data = s.recv(SIZE).decode(FORMAT).split('|')
    s.close()
    return server_data

def read_mail(command):
    global username
    header_only = 'False'
    if command.split(':')[0].strip() == 'read header':
        header_only = 'True'
    subject = command.split(':')[1].strip()
    s = connect_to_server()
    send_data_to_server(['read',username,subject,header_only],s)
    server_data = get_data_from_server_splitted(s)
    print(server_data[1])
    
def get_all_mails():
    global username
    s = connect_to_server()
    send_data_to_server(['get_all',username],s)
    server_data = get_data_from_server_splitted(s)
    for data in server_data:
        print(data)
        print('')

def delete_mail(command):
    global username
    subject = command.split(':')[1].strip()
    s = connect_to_server()
    send_data_to_server(['delete',username,subject],s)
    server_data = get_data_from_server_splitted(s)
    print(server_data[1])

def check_receiver():
    s = connect_to_server()
    receiver = input('Enter receiver: ')
    send_data_to_server(['check',receiver],s)
    server_data = get_data_from_server_splitted(s)
    return server_data, receiver

def forward_mail():
    global user_email
    server_data, receiver = check_receiver()
    print(server_data[1])
    if server_data[0] == 'True': 
        s = connect_to_server()
        subject = input('Enter subject: ')
        send_data_to_server(['forward',subject,user_email,receiver],s)
        server_data = get_data_from_server(s)
        print(server_data)

def compose_mail():
    global user_email
    server_data, receiver = check_receiver()
    print(server_data[1])
    if server_data[0] == 'True': 
        s = connect_to_server()
        subject = input('Enter subject: ')
        print('')
        print('Enter data. End data with an empty line containing (.): \n')
        message = ''
        while(True):
            text = input()
            if text == '.':
                break
            message += text + '\n'
        send_data_to_server(['compose',subject,user_email,receiver,message],s)
        server_data = get_data_from_server(s)
        print(server_data)
        
def search_mail(command):
    global username
    word = command.split(':')[1].strip()
    s = connect_to_server()
    send_data_to_server(['search',username,word],s)
    server_data = get_data_from_server_splitted(s)
    print(server_data[1])

def logout():
    global username,user_email
    s = connect_to_server()
    send_data_to_server(['logout'],s)
    server_data = get_data_from_server(s)
    print(server_data)
    username = ''
    user_email = ''

def menu():    
    print('Read mail ( read : <subject> )')
    print('Read mail header ( read header : <subject> )')
    print('Get all the mails in the system ( get_all )')
    print('Delete mail ( delete : <subject> )')
    print('Forward mail ( forward )')
    print('Compose mail ( compose )')
    print('Search mail ( search : <word> )')
    print('Logout ( logout )')
    print('')
    print('Enter command: ',end='')
    
def run_imap():
    global username, user_email
    s = connect_to_server()
    send_data_to_server(['handshake'],s)
    server_data = get_data_from_server(s)
    print(server_data)
    user_info = input()
    s = connect_to_server()
    send_data_to_server(['auth',user_info],s)
    server_data = get_data_from_server_splitted(s)
    print(server_data[1])
    if server_data[0] == 'True':
        username = user_info.split('|')[0].split('@')[0].strip()
        user_email =  user_info.split('|')[0].strip()
        while(True):
            menu()
            command = input()
            choice = command.split(' ')[0].lower()
            if choice == 'read':
                read_mail(command)
            elif choice == 'get_all':
                get_all_mails()
            elif choice == 'delete':
                delete_mail(command)
            elif choice == 'forward':
                forward_mail()
            elif choice == 'compose':
                compose_mail()
            elif choice == 'search':
                search_mail(command)
            elif choice == 'logout':
                logout()
                return
            else:
                print("Invalid command")
                continue
            input("Press Enter to continue...")


if __name__ == '__main__':
    while(True):
        command = input("Enter 'imap()' to login or 'quit' to quit the window : ").lower()
        if command == 'imap()':
            run_imap()
        elif command == 'quit':
            break