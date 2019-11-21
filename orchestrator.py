#!/usr/bin/python3
# -*- coding: utf-8; mode: python; -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import sys
import TrawlNet

class Orchestrator(TrawlNet.Orchestrator):
    def __init__(self, dw):
        self.dw = dw

    def downloadTask(self, url, current=None):
        print("Se recibe la URL: ",url)
        print("Se envia a downloader")
        msg = self.dw.addDownloadTask(url)
        print(msg)

        return msg


class Server(Ice.Application):
    def run(self, argv):
        print('Iniciando servidor Orchestrato')
        broker = self.communicator()
        prx_dw = broker.stringToProxy(argv[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(prx_dw)
        if not downloader:

            raise RuntimeError('Error')

        # Creamos el orchestrator
        server = Orchestrator(downloader)

        #Añadimos adapatdor
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        prx_orches = adapter.add(server, broker.stringToIdentity("orc"))

        print("",prx_orches)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

server = Server()
sys.exit(server.main(sys.argv))
