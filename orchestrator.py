#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

'''
Orchestrator
'''

import sys
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class OrchestratorsControl:
    ''' Orchestrators class '''

    orchestrators = {}
    files_update = {}

    def crear_orchestrator(self, topic_update, topic_orchestrator, broker):
        ''' Crear orchestrator'''
        self.orchestrator = OrchestratorI()
        identity = broker.getProperties().getProperty("Identity")
        self.orchestrator.orchestrator = self
        self.proxy_orchestrator = self.adapter.add(self.orchestrator, broker.stringToIdentity(identity))
        self.proxy_orchestrator = self.adapter.createDirectProxy(self.proxy_orchestrator.ice_getIdentity())

    def crear_file_update_event(self):
        ''' Crear FileUpdatesEventI '''
        self.file_updates = FileUpdatesEventI()
        self.file_updates.orchestrator = self
        self.file_updates_proxy = self.adapter.addWithUUID(self.file_updates)
        identity = self.file_updates_proxy.ice_getIdentity()
        self.file_updates_proxy = self.adapter.createDirectProxy(identity)
        self.file_topic.subscribeAndGetPublisher({}, self.file_updates_proxy)
   
    def crear_orchestrator_event(self):
        ''' Crear Orchestrator Event '''
        self.subscriptor = OrchestratorEventI()
        self.subscriptor.orchestrator = self
        self.proxy_subscriptor = self.adapter.addWithUUID(self.subscriptor)
        identity = self.proxy_subscriptor.ice_getIdentity()
        self.proxy_subscriptor = self.adapter.createDirectProxy(identity)
        self.topic_orchestrator.subscribeAndGetPublisher({}, self.proxy_subscriptor)
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.topic_orchestrator.getPublisher())

    def __init__(self, topic_update, topic_orchestrator, broker):
        ''' Constructor '''
        self.adapter = broker.createObjectAdapter("OrchestratorAdapter")
        self.transfer_factory = TrawlNet.TransferFactoryPrx.checkedCast(broker.propertyToProxy("TransferFactoryIdentity"))
        self.downloader_factory = TrawlNet.DownloaderFactoryPrx.checkedCast(broker.propertyToProxy("DownloaderFactoryIdentity"))
        self.downloader = self.downloader_factory.create()
        self.crear_orchestrator(topic_update, topic_orchestrator, broker)
        self.topic_orchestrator = topic_orchestrator
        self.file_topic = topic_update
        self.crear_orchestrator_event()
        self.crear_file_update_event()

    def tarea_de_descarga(self, url):
        ''' addDownloadTask'''
        return self.downloader.addDownloadTask(url)

    def nuevo_orchestrator(self, orchestrator):
        ''' Nuevo orchestrator '''
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("Hello its me %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator

    def saludo(self, orchestrator):
        ''' Decir hola '''
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("Hello!!! i am %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator
        orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.proxy_orchestrator))

    def inicializar(self):
        ''' Activar adaptador '''
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.proxy_orchestrator))

    def obtener_lista(self):
        ''' Obtener lista '''
        file_list = []
        for fhash in self.files_update:
            file_info_object = TrawlNet.FileInfo()
            file_info_object.hash = fhash
            file_info_object.name = self.files_update[fhash]
            file_list.append(file_info_object)
        return file_list

    def get_file(self, name):
        ''' get file'''
        return self.transfer_factory.create(name)

class OrchestratorI(TrawlNet.Orchestrator):
    '''
    OrchestratorI
    '''
    orchestrator = None


    def getFileList(self, current=None):
        ''' getFileList '''
        if self.orchestrator:
            return self.orchestrator.obtener_lista()
        return []

    def downloadTask(self, url, current=None):
        ''' downloadTask '''
        if self.orchestrator:
            return self.orchestrator.tarea_de_descarga(url)

    def announce(self, orchestrator, current=None):
        ''' Announce '''
        if self.orchestrator:
            self.orchestrator.nuevo_orchestrator(orchestrator)

    def getFile(self, name, current=None):
        ''' Get File Transfer'''
        if self.orchestrator:
            return self.orchestrator.get_file(name)


class FileUpdatesEventI(TrawlNet.UpdateEvent):
    '''
    FileUpdatesEventI
    '''
    orchestrator = None

    def newFile(self, file_info, current=None):
        '''newFile'''
        if self.orchestrator:
            file_hash = file_info.hash
            if file_hash not in self.orchestrator.files_update:
                print(file_info.name)
                print(file_info.hash)
                self.orchestrator.files_update[file_hash] = file_info.name


class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    '''
    OrchestratorEventI
    '''
    orchestrator = None

    def hello(self, orchestrator, current=None):
        ''' Saludo '''
        if self.orchestrator:
            self.orchestrator.saludo(orchestrator)


class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Servidor
    '''
    def run(self, argv):
        '''
        Init
        '''
        key = 'YoutubeDownloaderApp.IceStorm/TopicManager'
        topic_name_file = "UpdateEvents"
        topic_name_orchestrator = "OrchestratorSync"
        broker = self.communicator()
        proxy = broker.stringToProxy(key)

        if proxy is None:
            return None

        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101

        if not topic_mgr:
            return 2
     
        try:
            topic_update_event = topic_mgr.retrieve(topic_name_file)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic_update_event = topic_mgr.create(topic_name_file)

        try:
            topic_orchestrator_event = topic_mgr.retrieve(topic_name_orchestrator)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic_orchestrator_event = topic_mgr.create(topic_name_orchestrator)

        orchest = OrchestratorsControl(topic_update_event, topic_orchestrator_event, broker)
        orchest.inicializar()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0


ORCHEST = Server()
sys.exit(ORCHEST.main(sys.argv))
