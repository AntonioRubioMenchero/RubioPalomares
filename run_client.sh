#!/bin/sh

echo "Running client"

#nombre_interprete_python nombre_clase.py "<proxy_orchestrator>" "<url>" 
#./client.py $1 $2
#Ejecucion segun el interprete python3 cliente.py "proxy entre comillas" "youtube.com"
#./cliente.py $1 $2

#Se ejecuta ./run_client.sh "<proxy_orchestrator>" "<url>" 
./client.py "$1" "$2"
