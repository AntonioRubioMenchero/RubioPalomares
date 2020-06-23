#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet  #pylint: disable=E1101
import IceStorm
import os
from util import *

DIRECTORY = './files/'
KEY = 'IceStorm.TopicManager.Proxy'
auxfactory = ""


class TransferI(TrawlNet.Transfer):

    transfer_prx = None
    dicPeers = {}

    def __init__(self, receiver_factory):
        self.receiver_factory = receiver_factory
        self.sender_factory = auxfactory

    def createPeers(self, fileList, current):
        print('Creando Parejas')
        receiverList = []
        for element in fileList:
            try:
                sender_prx = self.sender_factory.create(element)
            except TrawlNet.FileDoesNotExistError as e:
                print(e)
            transfer = TrawlNet.TransferPrx.checkedCast(self.transfer_prx)

            print(transfer)

            if not transfer:
                raise RuntimeError('Invalid')

            receiver_prx = self.receiver_factory.create(
                element, sender_prx, transfer)
            print(receiver_prx)
            self.dicPeers.setdefault(element, [receiver_prx, sender_prx])
            receiverList.append(receiver_prx)
        return receiverList

    def destroyPeer(self, filename, current=None):
        receiver = self.dicPeers[filename][0]
        sender = self.dicPeers[filename][1]

        sender.destroy()
        receiver.destroy()

    def destroy(self, current=None):
        current.adapter.remove(current.id)
        print("SE HA ELIMINADO DEL ADAPTADOR")


class TransferFactoryI(TrawlNet.TransferFactory):
    # def __init__(self,peer_topic):
    #    # self.transfer_topic=transfer_topic
    #     self.peer_topic=peer_topic

    def newTransfer(self, receiver_factory, current=None):
        print('Creando Transfer')
        #print(self.peer_topic)
        #print(self.transfer_topic)

        transfer_servant = TransferI(receiver_factory)
        proxy = current.adapter.addWithUUID(transfer_servant)
        transfer_servant.transfer_prx = proxy

        return TrawlNet.TransferPrx.checkedCast(proxy)


class Server(Ice.Application):
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

        broker = self.communicator()

        factory = TransferFactoryI()
        adapter = broker.createObjectAdapter("TransferFactoryAdapter")
        proxy = adapter.add(factory,
                            broker.stringToIdentity("TransferFactory1"))
        print(proxy)

        topic_mng = self.get_topic_manager()
        if not topic_mng:
            print("Error en el proxy del canal de evento")
            return 2

        peer_broker = self.communicator()
        peer_adapter = peer_broker.createObjectAdapter("PeerEventAdapter")
        servant = PeerEventI()
        subscriber = peer_adapter.addWithUUID(servant)
        peer_topic = self.get_topic(topic_mng, 'PeerTopic')
        qos = {}

        peer_topic.subscribeAndGetPublisher(qos, subscriber)

        global auxfactory

        senderfactory_prx = self.communicator().stringToProxy(
            'SenderFactory1 -t -e 1.1 @ SenderFactory1')
        print(TrawlNet.SenderFactoryPrx.checkedCast(senderfactory_prx))
        auxfactory = TrawlNet.SenderFactoryPrx.checkedCast(senderfactory_prx)

        peer_adapter.activate()
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        print('Transfer acabado')

        return 0


class PeerEventI(TrawlNet.PeerEvent):
    def peerFinished(self, peer, current=None):
        peer.transfer.destroyPeer(peer.fileName)
        print("Pareja ha acabado de realizar descarga")


transfer = Server()
sys.exit(transfer.main(sys.argv))
