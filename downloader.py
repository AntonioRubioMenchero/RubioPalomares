#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import sys
import TrawlNet

import download_mp3 as d

class Server(Ice.Application):
    def run(self, argv):
        servidor = Downloader()
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy_server = adapter.add(servidor, broker.stringToIdentity("dw"))

        print(proxy_server,flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

class Downloader(TrawlNet.Downloader):
    def __init__(self):
        self.url=""

    def addDownloadTask(self, url, current=None):
        self.url=url
        print("Recibo",self.url)
        print("Descargando", self.url)

        return d.download_mp3(self.url)


server = Server()
sys.exit(server.main(sys.argv))
