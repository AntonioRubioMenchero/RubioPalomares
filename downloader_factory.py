#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader
'''

import sys
import hashlib
import os.path
import youtube_dl
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

import utils as utilidades


def hash_sha(filename):
    '''
    Crear hash sha256
    '''
    file_hash = hashlib.sha256()
    with open("./downloads/"+filename, "rb") as new_file:
        for chunk in iter(lambda: new_file.read(4096), b''):
            file_hash.update(chunk)
    return file_hash.hexdigest()

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
        properties = broker.getProperties()
        property_factory = properties.getProperty('DownloaderFactoryIdentity')

        downloader_publish = TrawlNet.UpdateEventPrx.uncheckedCast(topic.getPublisher())
        downloader = DownloaderFactoryI(downloader_publish)
        proxy = adapter.add(downloader, broker.stringToIdentity(property_factory))
        print(proxy, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

    def get_topic_manager(self):
        '''
        Get the topic manager
        '''
        key = 'YoutubeDownloaderApp.IceStorm/TopicManager'
        proxy = self.communicator().stringToProxy(key)
        if proxy is None:
            return None
        return IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101

class DownloaderFactoryI(TrawlNet.DownloaderFactory):
    '''
    DownloaderFactory
    '''
    def __init__(self,publisher):
        ''' Constructor '''
        self.publisher = publisher

    def create(self, current):
        ''' Create method '''
        downloader = DownloaderI(self.publisher)
        proxy = current.adapter.addWithUUID(downloader)
        print("New downloader #")
        return TrawlNet.DownloaderPrx.checkedCast(proxy)


class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    Downloader
    '''
    publisher = None

    def __init__(self, publisher):
        self.publisher = publisher

    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        Downloader
        '''

        file_task = utilidades.download_mp3(url)
        if not file_task:
            raise TrawlNet.DownloadError("Error en el proceso de descarga")
        fileInfo = TrawlNet.FileInfo()
        fileInfo.name = os.path.basename(file_task)
        fileInfo.hash = hash_sha(fileInfo.name)

        if self.publisher:
            self.publisher.newFile(fileInfo)
        return fileInfo

SERVER_DOWN = Server()
sys.exit(SERVER_DOWN.main(sys.argv))
