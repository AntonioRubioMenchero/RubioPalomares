#!/usr/bin/python3.6 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import IceStorm
Ice.loadSlice('-I. --all trawlnet.ice')
import TrawlNet  #pylint: disable=E1101



DIRECTORY = './files/'
KEY = 'IceStorm.TopicManager.Proxy'
AUXFACTORY = ''


class TransferI(TrawlNet.Transfer):

    transfer_prx = None
    transfer_topic = None
    dicPeers = {}

    def __init__(self, receiver_factory):
        self.receiver_factory = receiver_factory
        self.sender_factory = AUXFACTORY

    def createPeers(self, fileList, current):
        print('Creando Parejas')
        receiverList = []
        for element in fileList:
            try:
                sender_prx = self.sender_factory.create(element)
            except TrawlNet.FileDoesNotExistError as e:
                raise e

            transfer = TrawlNet.TransferPrx.checkedCast(self.transfer_prx)

            if not transfer:
                raise RuntimeError('Invalid')

            receiver_prx = self.receiver_factory.create(
                element, sender_prx, transfer)
            print(receiver_prx)
            self.dicPeers[element] = [receiver_prx, sender_prx]
            receiverList.append(receiver_prx)
        return receiverList

    def destroyPeer(self, filename, current=None):#pylint: disable = W0613
        receiver = self.dicPeers[filename][0]
        sender = self.dicPeers[filename][1]

        sender.destroy()
        receiver.destroy()

        del self.dicPeers[filename]

        print("Eliminamos pareja del diccionario asociada a " + filename + " receiver " + str(receiver) + " y sender " + str(sender))


        if not self.dicPeers:
            self.transfer_topic.transferFinished(TrawlNet.TransferPrx.checkedCast(
                self.transfer_prx))

    def destroy(self, current=None):
        current.adapter.remove(current.id)
        print("Se destruye el transfer " + str(self.transfer_prx))

class TransferFactoryI(TrawlNet.TransferFactory):

    def __init__(self, transfer_topic, current=None): #pylint: disable = W0613
        self.transfer_topic = transfer_topic

    def newTransfer(self, receiver_factory, current=None):#pylint: disable = W0613
        print('Creando Transfer')
        transfer_servant = TransferI(receiver_factory)
        proxy = current.adapter.addWithUUID(transfer_servant)
        transfer_servant.transfer_prx = proxy
        transfer_servant.transfer_topic = self.transfer_topic

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
    def get_topic(topic_mng, topic_Name):
        try:
            return topic_mng.retrieve(topic_Name)
        except IceStorm.NoSuchTopic:
            print("No topic {} found, creating".format(topic_Name))
            return topic_mng.create(topic_Name)

    def run(self, argv):#pylint: disable = W0613
        print('Transfer Manager Running')

        broker = self.communicator()

        topic_mng = self.get_topic_manager()
        if not topic_mng:
            print("Error en el proxy del canal de evento")
            return 2
        transfer_topic = self.get_topic(topic_mng, 'TransferTopic')


        publisher_transferEvent = transfer_topic.getPublisher()
        transfer_event = TrawlNet.TransferEventPrx.uncheckedCast(publisher_transferEvent) 

        factory = TransferFactoryI(transfer_event)
        adapter = broker.createObjectAdapter("TransferFactoryAdapter")
        proxy = adapter.add(factory,
                            broker.stringToIdentity("TransferFactory1"))
        print(proxy)


        peer_broker = self.communicator()
        peer_adapter = peer_broker.createObjectAdapter("PeerEventAdapter")
        servant = PeerEventI()
        subscriber = peer_adapter.addWithUUID(servant)
        peer_topic = self.get_topic(topic_mng, 'PeerTopic')
        qos = {}

        peer_topic.subscribeAndGetPublisher(qos, subscriber)

        global AUXFACTORY #pylint: disable = W0613

        senderfactory_prx = self.communicator().stringToProxy(
            'SenderFactory1 -t -e 1.1 @ SenderFactory1')
        print(TrawlNet.SenderFactoryPrx.checkedCast(senderfactory_prx))
        AUXFACTORY = TrawlNet.SenderFactoryPrx.checkedCast(senderfactory_prx)

        peer_adapter.activate()
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        print('Transfer acabado')

        return 0


class PeerEventI(TrawlNet.PeerEvent):
    def peerFinished(self, peer, current=None): #pylint: disable = W0613
        peer.transfer.destroyPeer(peer.fileName)
        print("Pareja ha acabado de realizar descarga")


transfer = Server()
sys.exit(transfer.main(sys.argv))
