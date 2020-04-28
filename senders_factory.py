#!/usr/bin/python3.6 -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet




class SenderI(TrawlNet.Sender):
    def __init__(self, name):
        self.name = name

    def receive(self,size):
        print("{0}: {1}".format(self.name, message))
        sys.stdout.flush()
        return 'recibido'
    


class SenderFactoryI(TrawlNet.SenderFactory):
    def __init__(self):


    def create(self, filename, current=None):

        if name in self.servants:
            raise 'Este Archivo ya esta en trasferencia'

        servant = SenderI(filename)
        proxy = current.adapter.addWithUUID(servant)

        return proxy.stringToIdentity(proxy)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        

        adapter = broker.createObjectAdapter("SenderFactoryAdapter")
       
        factory = SenderFactoryI()
        proxy = adapter.add(factory,broker.stringToIdentity("SenderFactory1"))
        print(proxy)


        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))