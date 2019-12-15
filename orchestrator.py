 #!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import re
import sys
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401

KEY = 'IceStorm.TopicManager.Proxy'

class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Server
    '''
    def run(self, argv):
        '''
        run
        '''
        broker = self.communicator()
        proxy = broker.propertyToProxy(KEY)

        if proxy is None:
            print("Error en el proxy")
            return None

        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101

        if not topic_mgr:
            print("Error en el topic mgr")
            return 2
     
        try:
            topic_update_event = topic_mgr.retrieve("UpdateEvents")
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic_update_event = topic_mgr.create("UpdateEvents")

        try:
            topic_orchestrator_event = topic_mgr.retrieve("OrchestratorSync")
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic_orchestrator_event = topic_mgr.create("OrchestratorSync")

        orchestrator = Orchestrator(broker, argv[1], topic_update_event, topic_orchestrator_event)
        orchestrator.run()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0


class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    '''
    OrchestratorEventI
    '''
    orchestrator = None

    def hello(self, me, current=None):
        ''' hello '''
        if self.orchestrator is not None:
            self.orchestrator.decir_hola(me)

class FileUpdatesEventI(TrawlNet.UpdateEvent):
    '''
    FileUpdatesEventI
    '''
    orchestrator = None

    def newFile(self, file_info, current=None):
        '''newFile'''
        if self.orchestrator:
            file_hash = file_info.hash
            if file_hash not in self.orchestrator.files:
                self.orchestrator.files[file_hash] = file_info.name
            else:
                print("File already exists!")


class OrchestratorI(TrawlNet.Orchestrator):
    '''
    OrchestratorI
    '''
    orchestrator = None

    def announce(self, orchestrator, current=None):
        ''' Announce '''
        if self.orchestrator is not None:
            self.orchestrator.nuevo_orchest(orchestrator)

    def getFileList(self, current=None):
        ''' getFileList '''
        if self.orchestrator is not None:
            return self.orchestrator.obtener_lista_canciones()
        return []

    def downloadTask(self, url, current=None):
        ''' downloadTask '''
        if self.orchestrator is not None:
            return self.orchestrator.download_task(url)


class Orchestrator:

    ''' Manage Orchestrators class '''

    qos = {}
    orchestrators = {}
    files= {}

    def crear_orchestrator(self, broker, downloader_proxy, topic_update, topic_orchestrator):
        ''' Crear orchestrator'''
        self.orchestrator = OrchestratorI()
        self.orchestrator.orchestrator = self
        self.proxy_orchestrator = self.adapter.addWithUUID(self.orchestrator)

    def crear_orchestratorEvent(self, broker):
        ''' Crear sincronizacion de orchestrators'''
        self.subscriptor = OrchestratorEventI()
        self.subscriptor.orchestrator = self
        self.proxy_subscriptor = self.adapter.addWithUUID(self.subscriptor)
        self.topic_orchestrator.subscribeAndGetPublisher(self.qos, self.proxy_subscriptor)
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.topic_orchestrator.getPublisher())

    def crear_file_update(self, broker):
        ''' Crear FileUpdatesEventI '''
        self.file_updates = FileUpdatesEventI()
        self.file_updates.orchestrator = self
        self.file_updates_proxy = self.adapter.addWithUUID(self.file_updates)
        self.file_topic.subscribeAndGetPublisher(self.qos, self.file_updates_proxy)

    def __init__(self, broker, downloader_proxy, topic_update, topic_orchestrator):
        ''' Constructor '''
        self.adapter = broker.createObjectAdapter("OrchestratorAdapter")
        self.crear_orchestrator(broker, downloader_proxy, topic_update, topic_orchestrator)
        self.downloader = TrawlNet.DownloaderPrx.checkedCast(broker.stringToProxy(downloader_proxy))
        self.topic_orchestrator = topic_orchestrator
        self.file_topic = topic_update
        self.crear_orchestratorEvent(broker)
        self.crear_file_update(broker)

    def download_task(self, url):
        ''' envio downloadTask '''
        return self.downloader.addDownloadTask(url)

    def decir_hola(self, orchestrator):
        ''' Decir hola a un orchestrator'''
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("Hola! %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator
        orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.proxy_orchestrator))

    def nuevo_orchest(self, orchestrator):
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("Hola! orchestrator %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator

    def run(self):
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.proxy_orchestrator))

    def obtener_lista_canciones(self):
        ''' Obtener lista '''
        file_list = []
        for fhash in self.files:
            file_info_object = TrawlNet.FileInfo()
            file_info_object.hash = fhash
            file_info_object.name = self.files[fhash]
            file_list.append(file_info_object)
        return file_list

    def __str__(self):
        return str(self.proxy_subscriptor)

ORCHEST = Server()
sys.exit(ORCHEST.main(sys.argv))
