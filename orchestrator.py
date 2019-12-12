#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Intermediario entre cliente y servidor
'''

import sys
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

songs = []

class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Servidor
    '''
    def get_topic_manager(self):
        key = "IceStorm.TopicManager.Proxy"
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            return None
        print("Using IceStorm in '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        '''
        Iniciar servidor
        '''
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print("Invalid proxy")
            return 2
        broker = self.communicator()
        proxy = broker.stringToProxy(argv[1])
        downloader_instance = TrawlNet.DownloaderPrx.checkedCast(proxy)
        if not downloader_instance:
            raise RuntimeError('Invalid proxy instance')

        evento_ficheros = UpdateEventI()
        files = evento_ficheros.files
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        evt_ficheros = adapter.addWithUUID(evento_ficheros)
        topic_name = "UpdateEvents"
        qos = {}

        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        topic.subscribeAndGetPublisher(qos, evt_ficheros)

        evento_orchestrators = OrchestratorEventI()
        evt_orchestrators = adapter.addWithUUID(evento_orchestrators)
        topic_orchestrator = "OrchestratorSync"
        qos = {}
        try:
            topicOrch = topic_mgr.retrieve(topic_orchestrator)
        except IceStorm.NoSuchTopic:
            topicOrch = topic_mgr.create(topic_orchestrator)

        topicOrch.subscribeAndGetPublisher(qos, evt_orchestrators)

        servant = OrchestratorI(files)
        proxy_orchestrator_instance = adapter.add(servant, broker.stringToIdentity("orchestrator"))

        servant.setProxy(proxy_orchestrator_instance)
        servant.setTopicandDownloader(downloader_instance, topicOrch)
        print(proxy_orchestrator_instance)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

class OrchestratorI(TrawlNet.Orchestrator): #pylint: disable=R0903
    '''
    Orchestrator Module
    '''
    files = {}

    def __init__(self, files):
        self.files = files

    def setTopicandDownloader(self, downloader, topic_orch):
        orchestrators = topic_orch.getPublisher()
        self.downloader = downloader
        obj_subscritos = TrawlNet.OrchestratorEventPrx.uncheckedCast(orchestrators)
        obj_subscritos.hello(TrawlNet.OrchestratorPrx.checkedCast(self.prx))

    def setProxy(self, prx):
        self.prx = prx

    def downloadTask(self, url, current=None): # pylint: disable=C0103, W0613
        '''
        Function download task
        '''
        print(url)
        return self.downloader.addDownloadTask(url)

    def getFileList(self, current=None):
        songs = []
        for fileHash in self.files:
            fileInfo = TrawlNet.FileInfo()
            fileInfo.hash = fileHash
            fileInfo.name = self.files[fileHash]
            songs.append(fileInfo)
        return songs

    def announce(self, orchestrator, current=None):
        print("Recibido ",orchestrator)

class UpdateEventI(TrawlNet.UpdateEvent):
    files = {}
  
    def newFile(self, fileInfo, current=None):
        fileHash = fileInfo.hash
        if fileHash not in self.files:
            print(fileInfo.name)
            print(fileInfo.hash)
            self.files[fileHash] = fileInfo.name
               
               
class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    def hello(self, orchestrator, current=None):
        orchestrator.announce(orchestrator)



SERVER = Server()
sys.exit(SERVER.main(sys.argv))
