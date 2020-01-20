#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Cliente
'''
import sys
import os
import binascii
import Ice # pylint: disable=E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

DOWNLOADS_DIRECTORY = './'

def transfer_request(file_name, orchestrator):
    remote_EOF = False
    BLOCK_SIZE = 1024
    transfer = None
    try:
        transfer = orchestrator.getFile(file_name)
    except TrawlNet.TransferError as e:
        print(e.reason)
        return 1

    with open(os.path.join(DOWNLOADS_DIRECTORY, file_name), 'wb') as file_:
        remote_EOF = False
        while not remote_EOF:
            data = transfer.recv(BLOCK_SIZE)
            if len(data) > 1:
                data = data[1:]
            data = binascii.a2b_base64(data)
            remote_EOF = len(data) < BLOCK_SIZE
            if data:
                file_.write(data)
        transfer.close()

    transfer.destroy()
    print('Transfer finished!')

class Client(Ice.Application): # pylint: disable=R0903
    '''
    Clase cliente
    '''
    def run(self, argv):
        '''
        Iniciar cliente
        '''
        broker = self.communicator()
        proxy = broker.stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if(len(argv)==2):
            print(orchestrator.getFileList())
        elif len(argv) == 4:
            if argv[2] == '--download':
                orchestrator.downloadTask(argv[3])
            elif argv[2] == '--transfer':
                transfer_request(argv[3], orchestrator)

        return 0

sys.exit(Client().main(sys.argv))
