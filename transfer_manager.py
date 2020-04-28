#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet
from util import *

DIRECTORY = './files/'

class TransferI(TrawlNet.Transfer):
    def __init__(self, name):
        self.name=name

    def createPeers(self,fileList,current=None):   
        RecieverList=[]
        for i in fileList:
            if(verifyfile(DIRECTORY,i)):
                receiver_servant=ReceiverI()
                reciever.filename=i
                RecieverList.append(reciever)
                print(i)
            else:
                print("El archivo " + i + " no se encuentra en el directorio " + DIRECTORY)
        return RecieverList
    
class TransferFactoryI(TrawlNet.TransferFactory):
    def __init__(self,name):
        self.name=name
    def newTransfer(self,transfer_n,current=None):
        transfer_servant= TrawlNet.TransferI(transfer_name)
        proxy = current.adapter.addWithUUID(transfer_servant)
        return TrawlNet.TransferPrx.checkedCast(proxy)


class Server(Ice.Application):
    def run(self,argv):

        broker = self.communicator()
        factory=TransferFactoryI('Factoria1')
        adapter = broker.createObjectAdapter("TransferFactoryAdapter")
        proxy=adapter.add(factory, broker.stringToIdentity("TransferFactory1"))
  
        
        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0



transfer= Server()
sys.exit(transfer.main(sys.argv))