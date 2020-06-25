#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import binascii
import os
import Ice
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet 
import IceStorm

DOWNLOADS_DIRECTORY = "./downloads/"
KEY = 'IceStorm.TopicManager.Proxy'


def get_files(argv):
    print('Archivos introducidos:')
    fileList = []
    for i in range(len(argv)):
        if i > 0:
            fileList.append(argv[i])
            print(argv[i])
    return fileList


class Client(Ice.Application):
    def get_topic_manager(self):
        proxy = self.communicator().propertyToProxy(KEY)
        if proxy is None:
            print("property {0} not set".format(KEY))
            return None
        print("Using IceStorm in: '%s'" % KEY)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    @staticmethod
    def get_topic(topic_mng, topicName):
        try:
            return topic_mng.retrieve(topicName)
        except IceStorm.NoSuchTopic:
            print("No topic {} found, creating".format(topicName))
            return topic_mng.create(topicName)

    def run(self, argv):
        print('Running Client')
        fileList = []
        broker = self.communicator()

        topic_mng = self.get_topic_manager()
        if not topic_mng:
            print('Invalid proxy')
            return 2

        peer_topic = self.get_topic(topic_mng, "PeerTopic")

        adapter = broker.createObjectAdapter('ReceiverFactoryAdapter')
        servant = ReceiverFactoryI(peer_topic)
        receiver_prx = adapter.add(servant,
                                   broker.stringToIdentity('ReceiverFactory1'))

        proxy = self.communicator().stringToProxy(
            'TransferFactory1 -t -e 1.1 @ TransferFactory1')
        factory = TrawlNet.TransferFactoryPrx.checkedCast(proxy)

        if not factory:
            raise RuntimeError('Invalid')

        ##ACTIVAMOS ADAPTADOR
        adapter.activate()

        


        topic_mng = self.get_topic_manager()
        if not topic_mng:
            print("Error en el proxy del canal de evento")
            return 2

        fileList = get_files(argv)

        transfer = factory.newTransfer(
            TrawlNet.ReceiverFactoryPrx.checkedCast(receiver_prx))
        print('Transfer: '+ str(transfer))

        transfer_broker = self.communicator()
        transfer_adapter = transfer_broker.createObjectAdapter("TransferEventAdapter")
        servant = TransferEventI(transfer, broker)
        transfer_topic = self.get_topic(topic_mng, 'TransferTopic')
        subscriber = transfer_adapter.addWithUUID(servant)
        qos = {}

        transfer_topic.subscribeAndGetPublisher(qos, subscriber)

        transfer_adapter.activate()

        try:
            receiverList = transfer.createPeers(fileList)
        except TrawlNet.FileDoesNotExistError as e:
            print("El fichero " + str(e) + " no existe")
            return 1

        for element in receiverList:
            element.start()

        broker.waitForShutdown()


        return 0


class ReceiverI(TrawlNet.Receiver):
    receiver = None
    peer_topic = None

    def __init__(self, filename, sender, transfer, current=None):
        self.filename = filename
        self.sender = sender
        self.transfer = transfer

    def start(self, current=None):
        print("Empieza la descarga del archivo " + self.filename)
        self.download_request(self.filename)

        peerInfo = TrawlNet.PeerInfo()
        peerInfo.transfer = self.transfer
        peerInfo.fileName = self.filename

        peerE = TrawlNet.PeerEventPrx.uncheckedCast(
            self.peer_topic.getPublisher())
        peerE.peerFinished(peerInfo)

    def destroy(self, current=None):
        print("Se destruye el receiver "+ str(self.receiver))
        current.adapter.remove(current.id)

    ##Código extraido del transfer_factory dado por los profesores en Conv Ordinaria
    def download_request(self, filename):
        remote_EOF = False
        BLOCK_SIZE = 1024
        # transfer = None

        # try:
        #     transfer = self.orchestrator.getFile(file_name)
        # except TrawlNet.TransferError as e:
        #     print(e.reason)
        #     return 1

        with open(os.path.join(DOWNLOADS_DIRECTORY, filename), 'wb') as file_:
            remote_EOF = False
            while not remote_EOF:
                data = self.sender.receive(BLOCK_SIZE)
                if len(data) > 1:
                    data = data[1:]
                data = binascii.a2b_base64(data)
                remote_EOF = len(data) < BLOCK_SIZE
                if data:
                    file_.write(data)
            self.sender.close()
        print('Descarga del archivo ' + filename + " finalizada")


class ReceiverFactoryI(TrawlNet.ReceiverFactory):
    def __init__(self, peer_topic, current=None):#pylint: disable = W0613
        self.peer_topic = peer_topic

    def create(self, filename, sender, transfer, current=None):#pylint: disable = W0613
        print("Creando Receiver")
        servant = ReceiverI(filename, sender, transfer)
        proxy = current.adapter.addWithUUID(servant)
        servant.receiver = proxy
        servant.peer_topic = self.peer_topic
        return TrawlNet.ReceiverPrx.checkedCast(proxy)


class TransferEventI(TrawlNet.TransferEvent):
    def __init__(self, transfer, broker):
        self.transfer = transfer
        self.broker = broker

    def transferFinished(self, transfer, current=None):#pylint: disable = W0613
        print('Se lanza evento finalizacion transfer ' + str(transfer))
        transfer.destroy()
        print('Cerrando programa ....')
        self.broker.shutdown()


sys.exit(Client().main(sys.argv))
