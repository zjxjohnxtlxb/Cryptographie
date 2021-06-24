#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_communication.py
#@auteur : Junxi ZHANG
#@date : 06/11/2020
#@description : Affaire avec RSA


from socket import *
import re
import os

from tp2_decoration import Detection
from tp2_affaire_outil import *


#class Communication
class Communication(object):
    """Le class couvrant des fonctions liés à la communication"""

    def __init__(self,cls,ADDR_RECV):
        self.__cls = cls
        self.ADDR_RECV = ADDR_RECV

    @property
    def cls(self):
        return self.__cls

    def recv(self):
        dirs = re.findall('./\w*',self.ADDR_RECV)[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        if os.path.exists(self.ADDR_RECV):
            os.remove(self.ADDR_RECV)
        socketfd = socket(AF_UNIX,SOCK_STREAM)
        socketfd.bind(self.ADDR_RECV)
        socketfd.listen(5)
        while True:
            connfd,addr = socketfd.accept()
            data_temp = connfd.recv(4096)
            if data_temp != bytes():
                self._stocker_recv_objet(data_temp)
            else:
                connfd.close()
        socketfd.close()

    def send(self,ADDR_SEND,data):
        clientfd = socket(AF_UNIX,SOCK_STREAM)
        clientfd.connect(ADDR_SEND)
        clientfd.send(data)
        clientfd.close()

    @Detection.type_alerte(name = str)
    def obtenir_objet(self,name):
        """Obtenir l'object de l'affaire.

        Parameters
        ----------
        name : str
            Name de l‘affaire cible
        Returns
        -------
        bytes
            L'object de l'affaire.

        """

        name = name.replace(".sock",".data")
        try:
            with open(name,mode='rb') as f:
                obj = f.read()
        except FileNotFoundError:
            obj = False
        return obj

    @Detection.type_alerte(name = str,obj = bytes)
    def stocker_objet(self,name,obj):
        """Stocker l'object de l'affaire.

        Parameters
        ----------
        name : str
            Name de l‘affaire cible.
        obj : bytes
            Object de l'affaire.

        Returns
        -------
        None

        """
        dirs = re.findall('./\w*',name)[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        name = name.replace(".sock",".data")
        with open(name,mode='wb') as f:
            f.write(obj)

    @Detection.type_alerte(obj = bytes)
    def _stocker_recv_objet(self,obj):
        obj_temp = self.cls.signature_N.Myrsakey.deballer_object(obj)
        print(obj_temp)
        if obj_temp['ADDR_VIEN'] not in self.cls.addr_list:
            self.cls.addr_list = obj_temp['ADDR_VIEN']
        ADDR_STO = self.cls.addr_construction(self.cls.name,\
        self.cls.addr_division(obj_temp['ADDR_VIEN']))
        self.stocker_objet(ADDR_STO,obj_temp['data'])
