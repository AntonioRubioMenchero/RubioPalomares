#!/bin/sh

./downloader.py --Ice.Config=download.config | tee proxy.out &

sleep 2

./orchestrator.py --Ice.Config=orche.config "$(head -1 proxy.out)"




