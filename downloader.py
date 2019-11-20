#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import sys
import TrawlNet



class Server(Ice.Application):
    def run(self, argv):
        servidor = Downloader()
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy_server = adapter.add(servidor, broker.stringToIdentity("dw"))

        print('',proxy_server)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

class Downloader(TrawlNet.Downloader):
    def __init__(self):
        self.url=""

    def addDownloadTask(self, url, current=None):
        self.url=url
        print("Recibo",url)
        print("Descargando", url)
        var = "downloader ha finalizado"
        return var


server = Server()
sys.exit(server.main(sys.argv))
