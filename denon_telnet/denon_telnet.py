#!/usr/bin/python2

import sys, time
from daemon import Daemon
from telnet import MyDebugServerFactory, MyProxyClientFactory, MyProxyServerFactory
from twisted.internet import reactor

class TelnetMultiplexer(Daemon):
       
    #-----------------------------------------------------------#
    # Read in command line arguments
    def run(self):
        remote_ip        = "192.168.1.xxx"
        remote_port      = 23
        local_port       = 23
        local_debug_port = 1357
        my_client = MyProxyClientFactory()
        my_server = MyProxyServerFactory()
        my_debug  = MyDebugServerFactory()
        my_server.local_server  = my_client
        my_server.debug_clients = my_debug
        my_client.local_clients = my_server
        my_client.debug_clients = my_debug
        reactor.connectTCP(remote_ip, remote_port, my_client)
        reactor.listenTCP(local_port, my_server)
        reactor.listenTCP(local_debug_port, my_debug)
        reactor.run()

if __name__ == "__main__":
    daemon = TelnetMultiplexer('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
            sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)