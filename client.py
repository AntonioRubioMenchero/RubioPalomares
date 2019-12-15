#!/usr/bin/env python3
# -*- coding: utf-8; -*-
'''
Implementacion cliente
'''

import sys
import Ice # pylint: disable=E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class Client(Ice.Application):
    '''
    Clase cliente
    '''
    lista = []
    orchestrator = None

    def descarga(self, url, current=None):
        ''' Descargar cancion '''
        print(self.orchestrator.downloadTask(url))
        

    def get_filelist(self, current=None):
        ''' obtener lista '''
        self.lista = self.orchestrator.getFileList()
        print(self.lista)

    def run(self, args):
        ''' Run '''
        proxy = self.communicator().stringToProxy(args[1])
        self.orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not self.orchestrator:
            raise RuntimeError("Invalid proxy")
        if len(args) == 3:
            self.descarga(args[2])
        elif len(args) == 2:
            self.get_filelist()




sys.exit(Client().main(sys.argv))
