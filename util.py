#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os



def verifyfile(repository,filename):
    dir=repository+filename
    return os.path.isfile(dir)
        

    