# Proyecto Descarga de Archivos

Proyecto para la Asignatura de Sistema Distribuidos de la Escuela Superior de Informatica de Ciudad Real, convocatoria extraordinaria
---
## Integrantes

 [Antonio Rubio Menchero](https://github.com/4Paloms)
 [Javier Palomares Garrido](https://github.com/JavierPalomaresGarrido)
---
## Link del repositorio
[Repositorio aquí](https://github.com/4Paloms/RubioPalomares.git)
---
## Tabla de Contenidos
- [Objetivos](#objetivos)
- [Enunciado](#enunciado)
- [Requisitos](#requisitos)
- [Ejecución](#ejecución)
- [Anotaciones](#anotaciones)
---
## Objetivos
1. El objetivo principal del proyecto es diseñar un sistema cliente-servidor que permita la descarga de ficheros. La implementación de este proyecto permitirá al alumno trabajar, mediante ZeroCIce, los siguientes aspectos:
 * Transparencia de localización
 * Manejo de canales de eventos
 * Despliegue de servidores
---
## Enunciado
El sistema estará compuesto por un cliente llamado FileDownloader con una factoría de receivers,un servidor con una factoría de transfers y otro servidor con una factoría de senders. El cliente, que recibirá como argumentos el nombre de los ficheros, solicitará una transferencia de N ficheros al servidor donde están ubicados los transfers. Este creará un transfer para controlar la transferencia,que a su vez creará una pareja receiver-sender para cada uno de los ficheros. Cuando todas lasparejas estén listas el cliente iniciará la transferencia, es decir, el envío entre las parejas. Losreceivers notificarán al transfer cuando hayan terminado, y este destruirá al receiver que envía lanotificación y a su sender compañero. Si todas las parejas han terminado, el tranfer informará al cliente (estará a la espera), que destruirá el transfer (en caso de que sea el suyo) y terminará su ejecución. Se tienen que tener en cuenta todos los fallos por acciones del cliente y controlarlos.

----
## Requisitos

1. Descargar e instalar `zeroc-ice-utils v.3.7.1-1`
1. Librerias necesarias para el funcionamiento de la practica:
    * `python3-zeroc-ice 3.7.1.1`

## Ejecución 

1. Lanzar en el primer terminal la parte de servidora donde vamos a encontrar tanto la factoria de envios como el manager de transferencias, toda la configuracion y creacion de archivos pertinentes para el correcto funciomaniento del programa:`./run_server.sh`
    * Icegrid (Registry)
    * IceStorm
    * Sender_Factory
    * Transfers_Manager
1. Lanzar en el segundo terminal la parte del cliente del sistema de esta manera: `./run_client.sh archivo1 archivo2 ` tanto archivo1 como archivo2 pueden ser reemplazados por cualquiera de los nombres de archivo que se encuentran en el directorio files.
1. Se dispone de varios archivos en el directorio files para poder realizar pruebas de descarga:
    * prueba
    * foto.jpeg
    * archivo.txt
1. Se dispone de una opcion para realizar limpieza de directorios creados automaticamente por los scripts `make clean`.
1. Los ficheros introduccidos por linea de comandos se podran encontrar en el directorio downloads en el caso de que se encuentren en el repositorio de archivos files. En el caso de que no se encuentren el sistema nos enviara un error.

---

## Anotaciones
1. Debido a que ICE realiza una 'carga en el aire', todas las llamadas sobre la interface de ICE generan un error a la hora de ejecutar pylint , por lo tanto, hemos optado por aplicar las lineas de código de desactivación debido a que no aclararia el codigo.
1. Queremos agradecer a nuestro profesor [Tobias Diaz Diaz-Chiron](https://github.com/ptobiasdiaz) el monitoreo y control del desarrollo de la practica.
