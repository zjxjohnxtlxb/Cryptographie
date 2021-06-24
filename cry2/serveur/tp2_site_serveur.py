#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_site_serveur.py
#@auteur : Junxi ZHANG
#@date : 08/11/2020
#@description : Affaire avec RSA


import sys
sys.path.append("..")
import os
import re

from tp2_role import site


def display():
    print("{:-^20}".format("site_serveur"))
    print("1.obtenir_keys_public_CA")
    print("2.send_keys_public")
    print("3.obtenir_keys_public")
    print("4.répondre_client")
    print("5.achete_verifi")
    print("6.transmet_verfi")
    print("q.quit")
    print("Enter the key you wanna try")
    print("_"*20)

def transmet_verfi(site_serveur):
    data = os.listdir('./'+site_serveur.name)
    data_temp =[]
    for i in data:
        i_temp = re.findall('^BANQUE_\w*(?=.data)',i)
        if len(i_temp) != 0 and i_temp[0] != 'addr_list':
            data_temp.append(i_temp[0])
    print(data_temp)
    entre = input("Entrez le name de banque que vous souhaitez transmetter :")
    while entre not in data_temp:
        print(data_temp)
        entre = input("Entrez le name qui existe :")
        if entre =='q':
            print("quitter")
            return
    facture = site_serveur.recv_object(entre)
    if facture:
        if isinstance(facture,str):
            print(facture)
            site_serveur.send_object(self.entre,facture)
        else:
            print("succès")
            site_serveur.transmet_verfi(facture)
    else:
        print("échec")


def show_keys_public(site_serveur):
    addr_list = site_serveur.keys_public_autre_list
    addr_list_temp =[]
    for i in addr_list:
        addr_list_temp.append(re.findall('(?!/)\w*(?=.sock)',i)[0])
    print(addr_list_temp)
    return addr_list_temp

def achete_verifi(site_serveur):
    data = os.listdir('./'+site_serveur.name)
    data_temp =[]
    for i in data:
        i_temp = re.findall('\w*(?=.data)',i)
        if len(i_temp) != 0 and i_temp[0] != 'addr_list':
            data_temp.append(i_temp[0])
    print(data_temp)
    entre = input("Entrez le name que vous souhaitez verifier :")
    while entre not in data_temp:
        print(data_temp)
        entre = input("Entrez le name qui existe :")
        if entre =='q':
            print("quitter")
            return
    facture = site_serveur.recv_object(entre)
    if facture:
        facture = site_serveur.verification(facture)
        if isinstance(facture,str):
            print(facture)
            site_serveur.send_object(entre,facture)
        else:
            print("succès")
            site_serveur.facture = facture
            site_serveur.entre = entre
            demande_verifi(site_serveur)
    else:
        print("échec")

def repondre_client(site_serveur):
    data = os.listdir('./'+site_serveur.name)
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
    client = site_serveur.recv_object(entre)
    if client:
        print("succès")
        site_serveur.envoyer_montant(client)
    else:
        print("échec")

def demande_verifi(site_serveur):
    value = re.compile('^BANQUE_\w*')
    entre = input("Entrez le name de banque:")
    while entre not in show_keys_public(site_serveur) or not value.match(entre):
        entre = input("Entrez le name de banque qui existe :")
        if entre =='q':
            print("quitter")
            return
    site_serveur.send_object(entre,site_serveur.facture)

def obtenir_keys_public_CA(site_serveur):
    print(site_serveur.keys_public_CA)

def send_keys_public(site_serveur):
    print(site_serveur.signature_N.Myrsakey.keys_public)
    print(site_serveur.signature_N.Myrsakey.keys_privee)
    site_serveur.send_keys_public()

def obtenir_keys_public(site_serveur):
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
    if site_serveur.obtenir_keys_public(entre):
        print("succès")
        print(site_serveur.keys_public_autre_list)
    else:
        print("échec")

def main():
    # value = re.compile('^[a-zA-Z]*$')
    # name = input(">>>le name de site:")
    # while not value.match(name):
    #     name = input(">>>Veuillez saisir un nom légal:")
    # montant = str(input(">>>ton montant de produit:"))
    # while not montant.isdigit():
    #     somme = str(input(">>>Veuillez saisir les chiffres:"))
    # site_serveur = site(name，somme)
    site_serveur = site("xx",1000)
    pid = os.fork()
    if pid == 0:
        site_serveur.communication.recv()
    else:
        display()
        while True:
            c = input(">>>")
            if c=='1':
                obtenir_keys_public_CA(site_serveur)
            if c=='2':
                send_keys_public(site_serveur)
            if c=='3':
                obtenir_keys_public(site_serveur)
            if c=='4':
                repondre_client(site_serveur)
            if c=='5':
                achete_verifi(site_serveur)
            if c=='6':
                transmet_verfi(site_serveur)
            if c=='q':
                sys.exit(0)
            display()

if __name__ =='__main__':
    main()
