# USAGE: python FileReciever.py

import socket, time, string, sys, urlparse, os
from threading import *

#------------------------------------------------------------------------

class StreamHandler ( Thread ):

    def __init__( this ):
        Thread.__init__( this )

    def run(this):
        this.process()

    def bind_tsock( this ):
        this.tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.tsock.bind(('', 9090))
        this.tsock.listen(1)
        print "[Transfer] Listening on port 9090"

    def accept_tsock( this ):
        this.tconn, this.taddr = this.tsock.accept()
        print "[Transfer] Receved connection from", this.taddr[0], "on port", this.taddr[1]
    
    def bind_csock( this ):
        this.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.csock.bind(('', 9091))
        this.csock.listen(1)
        print "[Control] Listening on port 9091"

    def accept_csock( this ):
        this.cconn, this.taddr = this.csock.accept()
        print "[Control] Got connection from", this.taddr
        
        while 1:
            data = this.cconn.recv(1024)
            if not data: break
            if data[0:4] == "SEND": this.filename = data[5:].split('\\')[-1]
            print "[Control] Receving %s" % this.filename
            break

    def transfer( this ):
        print "[Transfer] Starting media transfer for %s" % this.filename

        download_dir = "Downloads\\"

        if not os.path.isdir(download_dir):
            os.mkdir(download_dir)
        f = open(download_dir + this.filename,"wb")
        while 1:
            data = this.tconn.recv(1024)
            if not data: break
            f.write(data)
        f.close()

        print "[Transfer] Receved %s" % this.filename
        print "[Transfer] Closing Socket"
    
    def close( this ):
        this.cconn.close()
        this.csock.close()
        this.tconn.close()
        this.tsock.close()

    def process( this ):
        while 1:
            this.bind_csock()
            this.accept_csock()
            this.bind_tsock()
            this.accept_tsock()
            this.transfer()
            this.close()

#------------------------------------------------------------------------

s = StreamHandler()
s.start()