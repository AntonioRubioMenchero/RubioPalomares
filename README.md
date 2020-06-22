## Integrantes
 Antonio Rubio Menchero
 Javier Palomares Garrido

## Link del repositorio
[Repositorio aquí](https://github.com/4Paloms/RubioPalomares.git)

# Ejecucion del programa
A la hora de ejecutarlo tendremos varias alternativas:
1. Ejecucion Manual
2. Ejecucion mediante Make
3. Ejecucion mediante scripts sh.

## Ejecucion Registry

## Ejecucion IceStorm


## Ejecucion SenderFactory

``
python3 senders_factory.py --Ice.Config=senders.config
``
Nos imprimira en la terminal un proxy al que nos referiremos como senderfactory

## Ejecucion Transfer_manager

``
python3 transfer_manager.py --Ice.Config=transfers.config 
``
senderfactory seria una cadena de texto por lo tanto iria 'senderfactory'

Nos imprimira por terminal el proxy del transferfactory que usaremos en el cliente

## Ejecucion File_downloader
``
python3 file_downloader.py --Ice.Config=client.config archivo
``
transferfactory  sera el proxy que hemos obtenido por la terminal donde hemos ejecutado el transfer_manager

archivo sera el nombre del archivo que querramos probar a poder ser que se encuentre en el directorio ./files/ asi se apreciara de mejor manera el funcionamiento.



