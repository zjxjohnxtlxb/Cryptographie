#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_role.py
#@auteur : Junxi ZHANG
#@date : 07/11/2020
#@description : Affaire avec RSA


import re

from tp2_affaire_outil import *
from tp2_communication import *
from tp2_modele import Echeque

class role(object):

    def __init__(self,name):
        self.__name = name
        self.__Signature_N = Signature_N(Myrsakey(Miller_Rabin()))
        self.ADDR_RECV = self.addr_construction(self.name)
        self.ADDR_CA = self.addr_construction("CA")
        self.__keys_public_CA = None
        self.__keys_public_autre_list = dict()
        self.__addr_list = []
        super().__init__()
        self.__Communication = Communication(self,self.ADDR_RECV)

    def addr_construction(self,name1,name2='',name3='.sock'):
        if name2 == '':
            name2 = name1
        return './' + name1 + '/' + name2 + name3

    def addr_division(self,name,name2='.sock'):
        return re.findall('\w*(?='+name2+'$)',name)[0]

    @property
    def name(self):
        return self.__name

    @property
    def signature_N(self):
        return self.__Signature_N

    @property
    def communication(self):
        return self.__Communication

    @property
    def _keys_public(self):
        return self.signature_N.Myrsakey.keys_public

    @property
    def _keys_privee(self):
        return self.signature_N.Myrsakey.keys_privee

    @property
    def keys_public_autre_list(self):
        return self.__keys_public_autre_list

    @keys_public_autre_list.setter
    def keys_public_autre_list(self,value):
        self.__keys_public_autre_list.update(value)

    @property
    def addr_list(self):
        try:
            with open(self.addr_construction(self.name,'addr_list','.data'), mode='r', encoding='utf-8') as file:
                addr_list = file.read()
                if len(addr_list) == 0:
                    self.__addr_list = []
                else:
                    self.__addr_list = addr_list.split(',')
        except FileNotFoundError:
            self.__addr_list = []
        return self.__addr_list

    @addr_list.setter
    def addr_list(self,value):
        self.__addr_list.append(value)
        with open(self.addr_construction(self.name,'addr_list','.data'), mode='w', encoding='utf-8') as file:
            if len(self.__addr_list) != 0:
                for i,value in enumerate(self.__addr_list):
                    file.write(value)
                    if i != len(self.__addr_list) - 1:
                        file.write(',')


    def send_keys_public(self):
        key_temp = self.signature_N.Myrsakey.emballer_object(self._keys_public)
        obj_temp = {'ADDR_VIEN':self.ADDR_RECV,'data':key_temp}
        o_t =self.signature_N.Myrsakey.emballer_object(obj_temp)
        self.communication.send(self.ADDR_CA,o_t)

    def obtenir_keys_public(self,name):
        ADDR_VIEN = self.addr_construction('CA','P_'+name)
        obj = self.communication.obtenir_objet(ADDR_VIEN)
        if obj is False:
            return False
        a_temp = Myrsakey(Miller_Rabin(),self.keys_public_CA)
        obj_temp = a_temp.decrypt_affaire_c(obj)
        ADDR_RECV = self.addr_construction(name)
        self.keys_public_autre_list = {ADDR_RECV:self.signature_N.Myrsakey.deballer_object(obj_temp)}
        return True

    def _recv_keys_public_CA(self):
        obj_temp = self.communication.obtenir_objet(self.ADDR_CA)
        if obj_temp is False:
            return False
        self.__keys_public_CA = self.signature_N.Myrsakey.deballer_object(obj_temp)
        return True

    @property
    def keys_public_CA(self):
        if self.__keys_public_CA is None:
            self._recv_keys_public_CA()
        return self.__keys_public_CA

    def send_object(self,name,obj):
        ADDR_SEND = self.addr_construction(name)
        data_temp = self.signature_N.paquet_affaire(obj,self.keys_public_autre_list[ADDR_SEND])
        obj_temp = {'ADDR_VIEN':self.ADDR_RECV,'data':data_temp}
        o_t =self.signature_N.Myrsakey.emballer_object(obj_temp)
        self.communication.send(ADDR_SEND,o_t)

    def recv_object(self,name):
        ADDR_RECV_obj = self.addr_construction(self.name,name)
        obj_temp = self.communication.obtenir_objet(ADDR_RECV_obj)
        if obj_temp is False:
            return False
        ADDR_RECV = self.addr_construction(name)
        key_temp = self.keys_public_autre_list[ADDR_RECV]
        obj,sign = self.signature_N.depaquet_affaire(obj_temp,key_temp)
        verification = self.signature_N.lire_object(obj,sign)
        if verification is False:
            return False
        return verification


class CA(role):

    def __init__(self):
        super().__init__("CA")
        self._send_keys_public_CA()
        print("CA_serveur commence à travailler !")

    def _send_keys_public_CA(self):
        obj_temp = self.signature_N.Myrsakey.emballer_object(self._keys_public)
        self.communication.stocker_objet(self.ADDR_RECV,obj_temp)

    def obtenir_keys_public(self,name):
        ADDR_VIEN = self.addr_construction(name)
        if ADDR_VIEN in self.addr_list:
            ADDR_STO = self.addr_construction(self.name,self.addr_division(ADDR_VIEN))
            obj_temp = self.communication.obtenir_objet(ADDR_STO)
            if obj_temp is False:
                return False
            obj = self.signature_N.Myrsakey.deballer_object(obj_temp)
            self.keys_public_autre_list = {ADDR_VIEN:obj}
            return True
        else:
            return False

    def send_keys_public_CA(self,name):
        ADDR_VIEN = self.addr_construction(name)
        if ADDR_VIEN in self.keys_public_autre_list:
            obj_temp = self.signature_N.Myrsakey.emballer_object(self.keys_public_autre_list[ADDR_VIEN])
            o_t = self.signature_N.Myrsakey.encrypt_affaire_c(obj_temp)
            ADDR_SEND = self.addr_construction('CA','P_' + self.addr_division(ADDR_VIEN))
            self.communication.stocker_objet(ADDR_SEND,o_t)
            return True
        else:
            return False


class banque(role):

    def __init__(self,name):
        self.__name = "BANQUE_" + name
        self.__client_list = dict()
        super().__init__(self.name)
        print("banque_serveur commence à travailler !")
    @property
    def name(self):
        return self.__name

    @property
    def client_list(self):
        return self.__client_list

    @client_list.setter
    def client_list(self,value):
        self.__client_list.update(value)

    def creer_compte_client(self,client,num = 100):
        self.client_list = {client['name']:client['somme']}
        echeque_nouveau = Echeque(self.name,client,num)
        return echeque_nouveau

    def envoyer_echeque(self,client):
        self.send_object(client['name'],self.creer_compte_client(client))
        #self.creer_compte_client(client)

    def verification(self,facture):
        if facture['banque'] != self.name:
            return "Erreur banque"
        if facture['name'] not in self.client_list:
            return "Erreur client_banque"
        if not facture['is_used']:
            if facture['montant'] > self.client_list[facture['name']]:
                return "Somme insuffisant"
            self.client_list[facture['name']] -= facture['montant']
            facture['is_used'] = True
            return facture
        return "Erreur facture"

class client(role):

    def __init__(self,nom,prenom,somme):
        self.__nom = nom
        self.__prenom = prenom
        self.__somme = somme
        self.__echeque = None
        self.__facture = None
        self.__montant = 0
        super().__init__(self.name)
        print("client_serveur commence à travailler !")


    @property
    def nom(self):
        return self.__nom

    @property
    def prenom(self):
        return self.__prenom

    @property
    def name(self):
        self.__name = self.__nom + '_' + self.__prenom
        return self.__name

    @property
    def facture(self):
        return self.__facture

    @property
    def echeque_num(self):
        if self.__echeque == None:
            return 0
        else:
            return self.__echeque.num

    def demande_affaire(self,name):
        client = {'name':self.name,'somme':self.__somme}
        self.send_object(name,client)

    def recv_echeque(self,name):
        obj_temp = self.recv_object(name)
        if obj_temp is False:
            return False
        self.__echeque = obj_temp
        return True

    def recv_montant(self,name):
        obj_temp = self.recv_object(name)
        if obj_temp is False:
            return False
        self.__montant = obj_temp
        return True

    def ecrire_facture(self):
        if self.__echeque == None:
            return False
        if self.__montant == 0:
            return False
        facture = self.__echeque.ecrire_echeque(self.__montant)
        if facture:
            self.__facture = facture
            return True
        else:
            return False

    def verification(self,facture):
        if not isinstance(facture,str):
            if facture['montant'] == self.__montant:
                return True
            else:
                return False
        else:
            print(facture)
            return False

class site(role):

    def __init__(self,name,montant):
        self.__name = "SITE_" + name
        self.__montant = montant
        self.__client_list = list()
        super().__init__(self.__name)
        print("site_serveur commence à travailler !")

    @property
    def montant(self):
        return self.__montant

    @property
    def client_list(self):
        return self.__client_list

    @client_list.setter
    def client_list(self,value):
        self.__client_list.append(value)

    def envoyer_montant(self,client):
        if client['name'] not in self.client_list:
            self.client_list = client['name']
        self.send_object(client['name'],self.montant)

    def verification(self,facture):
        if facture['name'] not in self.client_list:
            return "Erreur client"
        if facture['montant'] != self.montant:
            return "Erreur montant"
        return facture

    def transmet_verfi(self,facture):
        if not isinstance(facture,str):
            facture['pay'] = True
        self.send_object(facture['name'],facture)
