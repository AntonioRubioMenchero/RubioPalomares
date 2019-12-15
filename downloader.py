#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader
'''

import sys
import hashlib
import os.path
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

from utilities import *

class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server
    '''
    #Iniciando servidor
    def run(self, argv): # pylint: disable=W0613,W0221
        '''
        Run Server
        '''
        topic_name = "UpdateEvents"

        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            return 2

        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic = topic_mgr.create(topic_name)

        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        servant = DownloaderI()
        servant.publisher = TrawlNet.UpdateEventPrx.uncheckedCast(topic.getPublisher())
        proxy_downloader = adapter.add(servant, broker.stringToIdentity("downloader"))
        print(proxy_downloader, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

    def get_topic_manager(self):
        '''
        Get the topic manager
        '''
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            return None
        return IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101


class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    Downloader
    '''
    publisher = None

    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        Downloader
        '''
        try:
            file_to_download = download_mp3(url)
        except:
            raise TrawlNet.DownloadError("Error downloading from yt")
        fileInfo = TrawlNet.FileInfo()
        fileInfo.name = os.path.basename(file_to_download)
        fileInfo.hash = get_id_youtube(url)

        if self.publisher is not None:
            self.publisher.newFile(fileInfo)
        return fileInfo

SERVER_DOWNLOADER = Server()
sys.exit(SERVER_DOWNLOADER.main(sys.argv))
