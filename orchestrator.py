#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Implementacion Orchestrator
'''

import sys
import Ice # pylint: disable=E0401, C0413
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401, C0413

class Orchestrator(TrawlNet.Orchestrator):
    ''' Clase orchestrador '''

    def __init__(self, downloader):
        ''' constructor '''
        self.dw = downloader

    def downloadTask(self, url, current=None):
        ''' Tarea de descargar '''
        print("Se recibe ", url)
        print("Se envia a downloader")
        msg = self.dw.addDownloadTask(url)
        return msg


class Server(Ice.Application):
    ''' Servidor '''
    def run(self, argv):
        ''' Run servidor en Ice '''

        broker = self.communicator()
        prx_dw = broker.stringToProxy(argv[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(prx_dw)
        if not downloader:
            raise RuntimeError('Error')

        server = Orchestrator(downloader)
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        prx_orches = adapter.add(server, broker.stringToIdentity("orc"))

        print("",prx_orches)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

server = Server()
sys.exit(server.main(sys.argv))
