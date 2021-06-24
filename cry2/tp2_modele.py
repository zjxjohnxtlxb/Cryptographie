#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_modele.py
#@auteur : Junxi ZHANG
#@date : 06/11/2020
#@description : Affaire avec RSA


class Echeque(object):
    """une classe Echeque."""

    def __init__(self,banque,client,num):
        self.__banque = banque
        self.__client = client
        self.__num = num
        super().__init__()

    class __facture(object):

        def __init__(self,cls,montant):
            self.__cls = cls
            self.__used = False
            self.__montant = montant
            self.__pay = False

        @property
        def client(self):
            return self.__cls.client

        @property
        def banque(self):
            return self.__cls.banque

        @property
        def montant(self):
            return self.__montant

        @property
        def is_used(self):
            return self.__used

        @is_used.setter
        def is_used(self,value):
            self.__used = value

        @property
        def pay(self):
            return self.__pay

        @pay.setter
        def pay(self,value):
            self.__pay = value

        def confirmation_pay(self):
            self.pay = True

        def use(self):
            self.is_used = True

    def ecrire_echeque(self,montant):
        if self.num > 0:
            self.num -= 1
            return self.__facture(self,montant)
        else:
            return False

    @property
    def client(self):
        return self.__client

    @property
    def banque(self):
        return self.__banque

    @property
    def num(self):
        return self.__num

    @num.setter
    def num(self,value):
        self.__num = value
