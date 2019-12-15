#!/bin/sh
#

PYTHON=python3

CLIENT_CONFIG=server.config

if [ $# -eq 2 ]; then
  $PYTHON client.py --Ice.Config=$CLIENT_CONFIG "$1" "$2"
fi

if [ $# -lt 2 ]; then
  $PYTHON client.py --Ice.Config=$CLIENT_CONFIG "$1"
  
fi




