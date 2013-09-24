#!/usr/bin/python

import sys
import os
import socket

def mainMenu():
	select = True
	while select:
		os.system('clear')
		print "NoSQLMap v0.01-by Russell Butturini(tcstool@gmail.com)"
		print "\n"
		print "1-Set options (do this first)"
		print "2-NoSQL DB Access Attacks"
		print "3-NoSQL Web App attacks"
		print "4-Exit"

		select = raw_input("Select an option:")

		if select == "1":
			options()

		elif select == "2":
			netAttacks()
		
		elif select == "3":
			webApps()

		elif select == "4":
			sys.exit()

def options():
	global host
	global uri
	global httpMethod

	select = True
	while select:	
		print "\n\n"
		print "Options"
		print "1-Set host/IP"
		print "2-Set URI Path"
		print "3-Set HTTP Request Method (GET/POST)"
		print "4-Back to main menu"

		select = raw_input("Select an option:")
		
		if select == "1":
			host = raw_input("Enter the host IP/DNS name: ")
			print "Target set to " + host + "\n"
			options()

		elif select == "2":
			uri = raw_input("Enter URI Path:")
			print "URI Path set to " + uri + "\n"
			options()

		elif select == "3":
			httpMethod = True
			while httpMethod:

				print "1-Send request as a GET"
				print "2-Send request as a POST"
				httpMethod = raw_input("Select an option: ")
			
				if httpMethod == "1":
					print "GET request set"
					options()

				elif httpMethod == "2":
					print "POST request set"
					options()
				else:
					print "Invalid selection"

		elif select == "4":
			mainMenu()


mainMenu()
