
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet


class Client(Ice.Application):
    def run(self, argv):
            fileList=[]

            print('Running Client')
            proxy = self.communicator().stringToProxy(argv[1])
            factory=TrawlNet.TransferFactoryPrx.checkedCast(proxy)

            if not factory:
              raise RuntimeError ('Invalid')
            

            print('Archivos introducidos:')

            for i in range(len(argv)):  
              if(i>1):
                fileList.append(argv[i])
                print(argv[i])

            return 0


            
class ReceiverI(TrawlNet.Receiver):
  def start(self):
    return 0

class ReceiverFactoryI(TrawlNet.ReceiverFactory):
  def __init__(self,name):
    self.name=name

  def create(self):
    return 0
  
sys.exit(Client().main(sys.argv))

        



