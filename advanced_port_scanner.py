#!/bin/python
import threading
import time
import socket
import sys
import os
import subprocess
from queue import Queue
from scapy.all import * # This library is useful and / or essential to networking using Python


print_lock = threading.Lock() # Threading lock prevents modification of a variable by two simulatenous processes. After mod1, Lock is released

# Define the target
if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1]) #Translate the hostname
else:
	print("Invalid amount of arguments.")
	print("Syntax: python3 port_scanner.py")

# Add a banner
print("-" * 50)
print("Multithreaded Stealth Scanner Active!")
print("Scanning target " + target)
start_clock = time.time() # The start time will be used to calculate the total time elapsed to perform the scan
print("Time started: " + str(start_clock))
print("-" * 50)


SYNACK = 0x12
def scanner(port):

	try:
		ip = IP(dst=target) # create a variable IP and use the IP function from scapy.all to set the destination to our target IP
		TCP_SYN = TCP(sport=RandShort(),dport=int(port),flags='S',seq=40) # RandShort() generates a source port on our machine
		# dport is target port, flags = 'S' is for stealth scan
		TCP_SYNACK = sr1(ip/TCP_SYN,timeout=0.5,verbose=1) # Send a packet and wait for a reply
		if not TCP_SYNACK or TCP_SYNACK.getlayer(TCP).flags != SYNACK: # SEQ Number for SYN-ACK
			print ("\n"+str(port)+":closed\n") # This is the response from our target, the HOST IP - expect RST
		else:
			print("\n"+str(port)+":open\n") # This is the response from our target, the HOST IP - expect a SYN-ACK response
	except KeyboardInterrupt:
		print("\nExiting program.")
		sys.exit()
		
def threader():
	while True:
		# get a worker from the queue
		worker = q.get()
		
		# run the scan function with the worker from the queue
		scanner(worker)
		
		# complete the job
		q.task_done()

# Create the queue and threader 
q = Queue()

# The amount of threads we will use
for n in range(100):
     t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     t.daemon = True

     # begins, must come after daemon definition
     t.start()


start = time.time()

# Assign 100 jobs
for worker in range(1,100):
    q.put(worker)

# Wait until the thread terminates.
q.join()

print("\nScanning Finished!")
print(('\nTime Elapsed:',time.time() - start_clock))
