#!/usr/bin/env python
# USAGE: python FileSender.py [file]

import sys, socket, os

class Server(object):
	"""	This class transmits a file using sockets to the client
		In the works
			SSL
			Make sure file is openable before transmit
			Split in to parts
			Errors
			Md5/ Sha1 hash parts and final
			Gui
			IPSCANNER
			Linux/Unix support
			Pretty Icons
	"""
	def __init__(self, arg):
		self.VERSION = 1.0
		self.HOST = 'localhost'
		self.MPORT = True
		self.CPORT = 9091
		self.TPORT = 9090
		self.IPSCANNER = True
		self.IPRANGE = "/24"
		
	def parse_options(options_file_name):
		COMMENT_CHAR = ';'
		OPTION_CHAR =  '='

		options_file = open(options_file_name)
		option_dict = {}

		for line in options_file:
			if COMMENT_CHAR in line:
				line, comment = line.split(COMMENT_CHAR, 1)
			if OPTION_CHAR in line:
				option, value = line.split(OPTION_CHAR, 1)

				option = option.rstrip()
				value = value.rstrip()
				option_dict[option] = value

		for key, value in option_dict.iteritems():
			if key == "Version":
				self.VERSION = value
			if key == "Multi Port":
				self.MPORT = value
			if key == "Control Port":
				self.CPORT = value
			if key == "Transfer Port":
				self.TPORT = value
			if key == "IPs to Scan":
				self.IPRANGE = value
			if key == "IP Scanner":
				self.IPSCANNER = value

	def send_information(option):
		self.control.send("Version: %s, Multi Port: %s, Control Port: %i, Transmit Port: %i" % (self.VERSION, self.MPORT, self.CPORT, self.TPORT))
		
	def server_init(HOST = 'localhost', CPORT = 9091, TPORT = 9090):

		FILE = sys.argv[1]

		control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		control.connect((HOST, TPORT))

		file_transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		file_transfer.connect((HOST, MPORT))

	def send_file(outgoing_file):
		to_send = open(outgoing_file, "rb")
		data = to_send.read()
		to_send.close()

		control.send("SENDING: " + FILE)

		file_transfer.send(data)

	def server_end():
		file_transfer.close()
		control.close()

if __name__ == '__main__':
	parse_options("Clinet.ini")