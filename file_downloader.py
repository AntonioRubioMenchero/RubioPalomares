
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import os
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet
import binascii

DOWNLOADS_DIRECTORY="./downloads/"

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

            try:
              receiverList=transfer.createPeers(fileList)
            except TrawlNet.FileDoesNotExistError as e:
              print (e)
              raise TrawlNet.FileDoesNotExistError("Error")
            

            for element in receiverList:
              element.start()
              element.destroy()
            
            transfer.destroy()

            return 0
    
            


            
class ReceiverI(TrawlNet.Receiver):
  def __init__(self,filename,sender,transfer):
    self.filename=filename
    self.sender=sender
    self.transfer=transfer

  def start(self,current=None):
    print("Empieza la descarga del archivo " + self.filename)
    self.download_request(self.filename)
   
    return "Descarga finalizada"
  def destroy(self,current=None):
    print("Se ha eliminado del adapter")
    current.adapter.remove(current.id)


  ##Código extraido del transfer_factory dado por los profesores en Conv Ordinaria
  def download_request(self, filename):
    remote_EOF = False
    BLOCK_SIZE = 1024
    # transfer = None

    # try:
    #     transfer = self.orchestrator.getFile(file_name)
    # except TrawlNet.TransferError as e:
    #     print(e.reason)
    #     return 1

    with open(os.path.join(DOWNLOADS_DIRECTORY, filename), 'wb') as file_:
        remote_EOF = False
        while not remote_EOF:
            data = self.sender.receive(BLOCK_SIZE)
            if len(data) > 1:
                data = data[1:]
            data = binascii.a2b_base64(data)
            remote_EOF = len(data) < BLOCK_SIZE
            if data:
                file_.write(data)
        self.sender.close()

    self.sender.destroy()
    print('Descarga del archivo ' + filename + " finalizada")
  


class ReceiverFactoryI(TrawlNet.ReceiverFactory):
  def create(self,filename,sender,transfer,current=None):
    print("Creando Receiver")
    servant = ReceiverI(filename,sender,transfer)
    proxy = current.adapter.addWithUUID(servant)
    return TrawlNet.ReceiverPrx.checkedCast(proxy)
    
  
sys.exit(Client().main(sys.argv))

        




