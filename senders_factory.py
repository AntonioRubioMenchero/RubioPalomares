#!/usr/bin/python3.6 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import binascii
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet

DIRECTORY = './files/'


class SenderI(TrawlNet.Sender):
    def __init__(self, filename):
        self.file_ = open(DIRECTORY + filename, 'rb')

    def close(self, current=None):
        self.file_.close()

    def destroy(self, current=None):
        current.adapter.remove(current.id)
        print("SE HA ELIMINADO DEL ADAPTADOR")

    def receive(self, size, current=None):
        print("Se empiezan a enviar datos con tamaño " + str(size))
        return str(binascii.b2a_base64(self.file_.read(size), newline=False))


class SenderFactoryI(TrawlNet.SenderFactory):
    def create(self, filename, current=None):
        try:
            open(DIRECTORY + filename, 'r')
        except TrawlNet.FileDoesNotExistError as e:
            print(e.info)
            raise TrawlNet.FileDoesNotExistError("Error")
        servant = SenderI(filename)
        proxy = current.adapter.addWithUUID(servant)
        return TrawlNet.SenderPrx.checkedCast(proxy)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("SenderFactoryAdapter")
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
