#!/bin/sh

./downloader.py --Ice.Config=download.config | tee salida_downloader.out &
arg=$(tail -1 salida_downloader.out)
./orchestrator.py --Ice.Config=orche.config "$arg"



