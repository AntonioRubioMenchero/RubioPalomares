#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Ice # pylint: disable=E0401, C0413
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401, C0413

class Cliente(Ice.Application):
    ''' Cliente '''
    def run(self, argv):
        ''' Iniciando cliente ice '''
        print('Iniciado cliente')
        proxy = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)
        if not orchestrator:
            raise RuntimeError('Error')
        msg = orchestrator.downloadTask(argv[2])
        print(msg)
        return 0

sys.exit(Cliente().main(sys.argv))
