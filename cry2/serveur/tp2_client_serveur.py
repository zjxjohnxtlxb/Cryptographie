#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_client_serveur.py
#@auteur : Junxi ZHANG
#@date : 08/11/2020
#@description : Affaire avec RSA


import sys
sys.path.append("..")
import os
import re

from tp2_role import client


def display():
    print("{:-^20}".format("client_serveur"))
    print("1.obtenir_keys_public_CA")
    print("2.send_keys_public")
    print("3.obtenir_keys_public")
    print("4.demande_echeque")
    print("5.recv_echeque")
    print("6.demande_achete")
    print("7.demande_verifi")
    print("8.recv_verifi")
    print("q.quit")
    print("Enter the key you wanna try")
    print("_"*20)

def recv_verifi(client_serveur):
    value = re.compile('^SITE_\w*')
    entre = input("Entrez le name de site:")
    while entre not in show_keys_public(client_serveur) or not value.match(entre):
        entre = input("Entrez le name de site qui existe :")
        if entre =='q':
            print("quitter")
            return
    facture = client_serveur.recv_object(entre)
    if client_serveur.verification(facture):
        print("succès")
    else:
        print("échec")

def show_keys_public(client_serveur):
    addr_list = client_serveur.keys_public_autre_list
    addr_list_temp =[]
    for i in addr_list:
        addr_list_temp.append(re.findall('(?!/)\w*(?=.sock)',i)[0])
    print(addr_list_temp)
    return addr_list_temp

def demande_echeque(client_serveur):
    value = re.compile('^BANQUE_\w*')
    entre = input("Entrez le name de banque:")
    while entre not in show_keys_public(client_serveur) or not value.match(entre):
        entre = input("Entrez le name de banque qui existe :")
        if entre =='q':
            print("quitter")
            return
    client_serveur.demande_affaire(entre)

def recv_echeque(client_serveur):
    value = re.compile('^BANQUE_\w*')
    entre = input("Entrez le name de banque:")
    while entre not in show_keys_public(client_serveur) or not value.match(entre):
        entre = input("Entrez le name de banque qui existe :")
        if entre =='q':
            print("quitter")
            return
    if client_serveur.recv_echeque(entre):
        print("succès")
    else:
        print("échec")

def demande_achete(client_serveur):
    value = re.compile('^SITE_\w*')
    entre = input("Entrez le name de site:")
    while entre not in show_keys_public(client_serveur) or not value.match(entre):
        entre = input("Entrez le name de site qui existe :")
        if entre =='q':
            print("quitter")
            return
        client_serveur.demande_affaire(entre)

def demande_verifi(client_serveur):
    value = re.compile('^SITE_\w*')
    entre = input("Entrez le name de site:")
    while entre not in show_keys_public(client_serveur) or not value.match(entre):
        entre = input("Entrez le name de site qui existe :")
        if entre =='q':
            print("quitter")
            return
    if client_serveur.recv_montant(entre):
        print("succès")
        if client_serveur.ecrire_facture():
            facture = {'name':client_serveur.name,'banque':client_serveur.facture.banque,'is_used':False,'montant':client_serveur.facture.montant,'pay':False}
            client_serveur.send_object(entre,facture)
    else:
        print("échec")


def obtenir_keys_public_CA(client_serveur):
    print(client_serveur.keys_public_CA)


def send_keys_public(client_serveur):
    print(client_serveur.signature_N.Myrsakey.keys_public)
    client_serveur.send_keys_public()

def obtenir_keys_public(client_serveur):
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
    if client_serveur.obtenir_keys_public(entre):
        print("succès")
        print(client_serveur.keys_public_autre_list)
    else:
        print("échec")


def main():
    # value = re.compile('^[a-zA-Z]*$')
    # nom = input(">>>ton nom:")
    # while not value.match(nom):
    #     nom = input(">>>Veuillez saisir un nom légal:")
    # prenom = input(">>>ton prenom:")
    # while not value.match(prenom):
    #     prenom = input(">>>Veuillez saisir un prénom légal:")
    # somme = str(input(">>>ton somme:"))
    # while not somme.isdigit():
    #     somme = str(input(">>>Veuillez saisir les chiffres:"))
    #client_serveur = client(nom,prenom,somme)
    client_serveur = client("A","s",1000)
    pid = os.fork()
    if pid == 0:
        client_serveur.communication.recv()
    else:
        display()
        while True:
            c = input(">>>")
            if c=='1':
                obtenir_keys_public_CA(client_serveur)
            if c=='2':
                send_keys_public(client_serveur)
            if c=='3':
                obtenir_keys_public(client_serveur)
            if c=='4':
                demande_echeque(client_serveur)
            if c=='5':
                recv_echeque(client_serveur)
            if c=='6':
                demande_achete(client_serveur)
            if c=='7':
                demande_verifi(client_serveur)
            if c=='8':
                recv_verifi(client_serveur)
            if c=='q':
                sys.exit(0)
            display()

if __name__ =='__main__':
    main()
