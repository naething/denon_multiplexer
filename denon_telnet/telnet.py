from twisted.internet import protocol

#-----------------------------------------------------------#
# Normal Clients
#-----------------------------------------------------------#

#-----------------------------------------------------------#
# Protocal for Incoming Connections
class MyProxyServer(protocol.Protocol):

    def dataReceived(self, data):
        #print "Received (client:", self.transport.getHost(), ")", data
        for online in self.factory.local_server.online:
            online.transport.write(data)
        for online in self.factory.debug_clients.online:
            online.transport.write("(client:" + str(self.transport.getHost()) + ")" + data + "\n")

    def connectionMade(self):
        self.factory.online.append(self)
        print self.transport.getHost()

    def connectionLost(self, reason):
        self.factory.online.remove(self)


#-----------------------------------------------------------#
# Incoming Connections Factory
class MyProxyServerFactory(protocol.ServerFactory):
    protocol = MyProxyServer

    def __init__(self):
        self.online = []
        self.local_server = []
        self.debug_clients = []
    
#-----------------------------------------------------------#
# Debug Clients
#-----------------------------------------------------------#

#-----------------------------------------------------------#
# Protocal for Incoming Connections
class MyDebugServer(protocol.Protocol):

    def dataReceived(self, data):
        # Here we can add some command handling
        pass

    def connectionMade(self):
        self.factory.online.append(self)
        print self.transport.getHost()

    def connectionLost(self, reason):
        self.factory.online.remove(self)

#-----------------------------------------------------------#
# Incoming Connections Factory
class MyDebugServerFactory(protocol.ServerFactory):
    protocol = MyDebugServer

    def __init__(self):
        self.online = []

#-----------------------------------------------------------#
# The Device We are Multiplexing
#-----------------------------------------------------------#

#-----------------------------------------------------------#
# Telnet Client
class MyProxyClient(protocol.Protocol):    
    def connectionMade(self):
        self.factory.online.append(self)
    
    def dataReceived(self, data):
        #print "Received (server):", data
        for online in self.factory.local_clients.online:
            online.transport.write(data)
        for online in self.factory.debug_clients.online:
            online.transport.write("(server)" + data + "\n")
        
    def connectionLost(self, reason):
        print "connection lost"
        self.factory.online.remove(self)

#-----------------------------------------------------------#
# Telnet Client Factory
class MyProxyClientFactory(protocol.ReconnectingClientFactory):
    
    def startedConnecting(self, connector):
        print "Starting to connect"

    def buildProtocol(self, addr):
        print "Connected"
        p = MyProxyClient()
        p.factory = self
        self.resetDelay()
        return p

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def __init__(self):
        self.online = []
        self.local_clients = []
        self.debug_clients = []