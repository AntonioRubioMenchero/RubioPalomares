#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet


class Cliente(Ice.Application):

    def run(self, argv):
        print('iniciado cliente')
        proxy = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError('Proxy no valido')

        msg = orchestrator.downloadTask(argv[2])
        print(msg)
        return 0

sys.exit(Cliente().main(sys.argv))
