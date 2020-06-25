#!/usr/bin/python3.6 -u
# -*- coding: utf-8 -*-


import binascii
import sys
import os.path
import Ice
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet

DIRECTORY = './files/'


class SenderI(TrawlNet.Sender):
    def __init__(self, filename):
        self.filename = open(DIRECTORY + filename, 'rb')

    def close(self, current=None):#pylint: disable = W0613
        self.filename.close()

    def destroy(self, current=None):#pylint: disable = W0613
        current.adapter.remove(current.id)
        print("Se destruye el sender")

    def receive(self, size, current=None):#pylint: disable = W0613
        print("Se empiezan a enviar datos con tamaño " + str(size))
        return str(binascii.b2a_base64(self.filename.read(size), newline=False))


class SenderFactoryI(TrawlNet.SenderFactory):
    def create(self, filename, current=None):#pylint: disable = W0613
        if not os.path.exists(os.path.join(DIRECTORY, filename)):
            raise TrawlNet.FileDoesNotExistError("Error " + filename + " no existe")
        servant = SenderI(filename)
        proxy = current.adapter.addWithUUID(servant)
        return TrawlNet.SenderPrx.checkedCast(proxy) 

class Server(Ice.Application):
    def run(self, argv): #pylint: disable = W0613
        print("Sender Running")
        broker = self.communicator()
        adapter = broker.createObjectAdapter('SenderFactoryAdapter')
        factory = SenderFactoryI()
        proxy = adapter.add(factory, broker.stringToIdentity("SenderFactory1"))
        print(proxy)

        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        print('SenderFactory Finalizado')

        return 0


server = Server()
sys.exit(server.main(sys.argv))
