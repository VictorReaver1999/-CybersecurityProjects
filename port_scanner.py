#!/bin/python

import sys
import socket
from datetime import datetime

# Define the target
if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1]) #Translate the hostname
else:
	print("Invalid amount of argument.")
	print("Syntax: python3 port_scanner.py <ip>")

# Add a banner
print("-" * 50)
print("Scanning target " + target)
print("Time started: " + str(datetime.now()))
print("-" * 50)

try:
	for port in range(1,200):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#AF_INET is IPV4
		#SOCK_STREAM is PORT
		socket.setdefaulttimeout(1) 
		# if port not connectible, we timeout after 1 second of waiting
		result = s.connect_ex((target, port)) #returns an error indicator if it is closed, otherwise 0
		if result = 0:
			print("Port {} is open".format(port))
		s.close()

except KeyboardInterrupt:
	print("\nExiting program.")
	sys.exit()

except socket.gaierror:
	print("Hostname could not be resolved.")
	sys.exit()
	
except socket.error:
	print("Couldn't connect to server")
	sys.exit()
