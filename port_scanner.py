'''
Port Scanners are primarily used for Penetration Testing and Information Gathering.
Essentially, we are looking for open ports in a host for one of two reasons.
To ensure our servers are secure or to exploit those of someone else.
An unnecessarily opened port means vulnerability and comes with a lack of security.
Note that port scanning is illegal for networks that don't belong to you.
'''

import socket
import threading
from queue import Queue

# Creates a First In First Out queue
queue = Queue() 

# WELL_KNOW_PORT_LIST = range(1, 1024)
WELL_KNOW_PORT_LIST = range(1, 65535)
ROUTER_IP_ADDRESS = '192.168.23.1'
HTTP_PORT_NUMBER = '80'

def scan_port(ip_address, port):
    try:
        # SOCK_STREAM means we're using TCP instead of UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # target is our IP address
        socket.create_connection((ip_address, port))
        return True 
    except socket.error as err:
        # print("Socket creation failed with error: %s" %(err))
        return False

def fill_queue(port_list):
    '''
    Helper function to help us fill in the queue with a list of port numbers
    '''
    for port in port_list:
        queue.put(port)

def worker():
    '''
    Our worker function which each thread will run
    '''
    while not queue.empty():
        port = queue.get() # Get the next element in the queue
        if scan_port(ip_address=ROUTER_IP_ADDRESS, port=str(port)):
            print("Port %s is opened" %(port))
            open_ports.append(str(port))

###########################################################################################

fill_queue(port_list=WELL_KNOW_PORT_LIST)
open_ports = []
thread_list = []
number_of_threads = 200

# Step 1 - Spawn the number of threads so that we can scare faster based on the number of threads we want
for t in range(number_of_threads):
    # Note that we are not calling the worker, we are just passing it as reference
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

# Step 2 - Start all the threads
for thread in thread_list:
    thread.start()

# Step 3 - Wait for all the threads to finish
for thread in thread_list:
    # the join statement wait for the thread is done until it continues with the code
    thread.join()

# Step 4 - Show results
print('Open ports are: ', open_ports)