#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os



def verifyfile(repository,filename):
    print('Verificando archivo ' + filename + ' en el directorio ' + repository)
    dir=repository+filename
    return os.path.isfile(dir)
        

    