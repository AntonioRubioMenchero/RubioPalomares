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
