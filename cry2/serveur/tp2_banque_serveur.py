#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_banque_serveur.py
#@auteur : Junxi ZHANG
#@date : 08/11/2020
#@description : Affaire avec RSA


import sys
sys.path.append("..")
import os
import re

from tp2_role import banque


def display():
    print("{:-^20}".format("banque_serveur"))
    print("1.obtenir_keys_public_CA")
    print("2.send_keys_public")
    print("3.obtenir_keys_public")
    print("4.répondre_client")
    print("5.achete_verifi")
    print("q.quit")
    print("Enter the key you wanna try")
    print("_"*20)

def achete_verifi(banque_serveur):
    data = os.listdir('./'+banque_serveur.name)
    data_temp =[]
    for i in data:
        i_temp = re.findall('\w*(?=.data)',i)
        if len(i_temp) != 0 and i_temp[0] != 'addr_list':
            data_temp.append(i_temp[0])
    print(data_temp)
    entre = input("Entrez le name de site que vous souhaitez verifier :")
    while entre not in data_temp:
        print(data_temp)
        entre = input("Entrez le name de site qui existe :")
        if entre =='q':
            print("quitter")
            return
    facture = banque_serveur.recv_object(entre)
    if facture:
        facture = banque_serveur.verification(facture)
        if isinstance(facture,str):
            print(facture)
        else:
            print("succès")
        banque_serveur.send_object(entre,facture)
    else:
        print("échec")

def repondre_client(banque_serveur):
    data = os.listdir('./'+banque_serveur.name)
    data_temp =[]
    for i in data:
        i_temp = re.findall('\w*(?=.data)',i)
        if len(i_temp) != 0 and i_temp[0] != 'addr_list':
            data_temp.append(i_temp[0])
    print(data_temp)
    entre = input("Entrez le name que vous souhaitez répondre :")
    while entre not in data_temp:
        print(data_temp)
        entre = input("Entrez le name qui existe :")
        if entre =='q':
            print("quitter")
            return
    client = banque_serveur.recv_object(entre)
    if client:
        print("succès")
        banque_serveur.client = client
        banque_serveur.envoyer_echeque(client)
        print(banque_serveur.client_list)
    else:
        print("échec")

def obtenir_keys_public_CA(banque_serveur):
    print(banque_serveur.keys_public_CA)

def send_keys_public(banque_serveur):
    print(banque_serveur.signature_N.Myrsakey.keys_public)
    banque_serveur.send_keys_public()

def obtenir_keys_public(banque_serveur):
    data = os.listdir('./CA')
    data_temp =[]
    for i in data:
        i_temp = re.findall('P_\w*(?=.data)',i)
        if len(i_temp) != 0:
            data_temp.append(i_temp[0].replace('P_',''))
    print(data_temp)
    entre = input("Entrez le name que vous souhaitez avoir sa clé :")
    while entre not in data_temp:
        print(data_temp)
        entre = input("Entrez le name qui existe :")
        if entre =='q':
            print("quitter")
            return
    if banque_serveur.obtenir_keys_public(entre):
        print("succès")
        print(banque_serveur.keys_public_autre_list)
    else:
        print("échec")

def main():
    # value = re.compile('^[a-zA-Z]*$')
    # name = input(">>>le name de banque:")
    # while not value.match(name):
    #     name = input(">>>Veuillez saisir un nom légal:")
    #banque_serveur = banque(name)
    banque_serveur = banque("lel")
    pid = os.fork()
    if pid == 0:
        banque_serveur.communication.recv()
    else:
        display()
        while True:
            c = input(">>>")
            if c=='1':
                obtenir_keys_public_CA(banque_serveur)
            if c=='2':
                send_keys_public(banque_serveur)
            if c=='3':
                obtenir_keys_public(banque_serveur)
            if c=='4':
                repondre_client(banque_serveur)
            if c=='5':
                achete_verifi(banque_serveur)
            if c=='q':
                sys.exit(0)
            display()

if __name__ =='__main__':
    main()
