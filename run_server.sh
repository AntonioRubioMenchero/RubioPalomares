#!/bin/sh


#Ejecutar IceBox
rm -r IceStorm/

mkdir -p IceStorm/

sleep 2

sudo icebox --Ice.Config=icebox.config &

sleep 2

./downloader.py --Ice.Config=server.config | tee proxy.out &

sleep 2

prx=$(head -1 proxy.out)

./orchestrator.py --Ice.Config=server.config "$prx" &

sleep 2

./orchestrator.py --Ice.Config=server.config "$prx"
