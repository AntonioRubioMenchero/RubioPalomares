#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet
import IceStorm
from util import *

DIRECTORY = './files/'
auxfactory=""

class TransferI(TrawlNet.Transfer):
        
    transfer_prx = None
    
    def __init__(self, receiver_factory):
        self.receiver_factory=receiver_factory
        self.sender_factory=auxfactory

    def createPeers(self,fileList,current):
        print('Creando Parejas') 
        receiverList=[]
        for element in fileList:
            if(verifyfile(DIRECTORY,element)):
                sender_prx=self.sender_factory.create(element)
                transfer=TrawlNet.TransferPrx.checkedCast(self.transfer_prx)
                print(transfer)
                if not transfer:
                    raise RuntimeError ('Invalid')
                print("Llegamos")
                receiver=self.receiver_factory.create(element,sender_prx,transfer)
                print(receiver)
                receiverList.append(receiver)
            else:
                print("El archivo " + element + " no se encuentra en el directorio " + DIRECTORY)
        return receiverList
        
    def destroyPeer(self,current):
        pass
    def destroy(self):
        pass

    
class TransferFactoryI(TrawlNet.TransferFactory):
    def newTransfer(self,receiver_factory,current=None):
        print('Creando Transfer')
        transfer_servant= TransferI(receiver_factory)
        proxy=current.adapter.addWithUUID(transfer_servant)
        transfer_servant.transfer_prx=proxy
        return TrawlNet.TransferPrx.checkedCast(proxy)

class Server(Ice.Application):
    def run(self,argv):
        

        broker = self.communicator()
        properties=broker.getProperties()
        factory=TransferFactoryI()
        adapter = broker.createObjectAdapter("TransferFactoryAdapter")
        proxy=adapter.add(factory, broker.stringToIdentity("TransferFactory1"))
        print(proxy)

        global auxfactory


        senderfactory_prx=self.communicator().stringToProxy(argv[1])
        print(TrawlNet.SenderFactoryPrx.checkedCast(senderfactory_prx))
        auxfactory=TrawlNet.SenderFactoryPrx.checkedCast(senderfactory_prx)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        print('Transfer acabado')

       

        return 0


class PeerInfo(TrawlNet.PeerInfo):
    def __init__(self,transfer=None,filename=''):
        self.transfer=transfer
        filename=''
        

transfer= Server()
sys.exit(transfer.main(sys.argv))