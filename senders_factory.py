#!/usr/bin/python3.6 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import binascii
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet




class SenderI(TrawlNet.Sender):
    def __init__(self,filename):
        self.filename=filename
    def close(self,current):
        self.filename.close()
    def destroy(self,current):
        current.adapter.remove(Ice.stringToIdentity(self))
    def receive(self,size,current):
        return str(binascii.b2a_base64(self.filename.read(size),newline=False))
    


class SenderFactoryI(TrawlNet.SenderFactory):
    def create(self, filename, current=None):
        servant = SenderI(filename)
        proxy = current.adapter.addWithUUID(servant)
        print("Estoy aqui")
        return TrawlNet.SenderPrx.checkedCast(proxy)


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

        print('SenderFactory Finalizado')

        return 0


server = Server()
sys.exit(server.main(sys.argv))