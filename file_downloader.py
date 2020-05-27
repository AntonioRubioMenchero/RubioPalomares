
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet

def get_files(argv):
      fileList=[]
      for i in range(len(argv)): 
        if(i>1):
          fileList.append(argv[i])
          print(argv[i])
      return fileList

class Client(Ice.Application):
    def run(self, argv):
            print('Running Client')
            fileList=[]

            broker=self.communicator()
            adapter=broker.createObjectAdapter('ReceiverFactoryAdapter')
            servant=ReceiverFactoryI()
            receiver_prx=adapter.add(servant,broker.stringToIdentity('ReceiverFactory1'))


           

            proxy=self.communicator().stringToProxy(argv[1])
            factory=TrawlNet.TransferFactoryPrx.checkedCast(proxy)

            

            if not factory:
              raise RuntimeError ('Invalid')

            ##ACTIVAMOS ADAPTADOR
            adapter.activate()

            print('Archivos introducidos:')

            fileList=get_files(argv)
            

            transfer=factory.newTransfer(TrawlNet.ReceiverFactoryPrx.checkedCast(receiver_prx))
            print(transfer)
            List=transfer.createPeers(fileList)
            print(List)

            adapter.activate()

            return 0
    
            


            
class ReceiverI(TrawlNet.Receiver):
  def __init__(self,filename,sender,transfer):
    self.filename=filename
    self.sender=sender
    self.transfer=transfer

  def start(self):
    return 0

class ReceiverFactoryI(TrawlNet.ReceiverFactory):
  def create(self,filename,sender,transfer,current=None):
    print("Creando Receiver")
    servant = ReceiverI(filename,sender,transfer)
    proxy = current.adapter.addWithUUID(servant)
    return TrawlNet.ReceiverPrx.checkedCast(proxy)
    
  
sys.exit(Client().main(sys.argv))

        




