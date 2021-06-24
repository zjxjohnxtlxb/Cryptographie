#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_CA_serveur.py
#@auteur : Junxi ZHANG
#@date : 08/11/2020
#@description : Affaire avec RSA


import sys
sys.path.append("..")
import os
import re

from tp2_role import CA


def display():
    print("{:-^20}".format("CA_serveur"))
    print("1.show_keys_public")
    print("2.send_keys_public")
    print("q.quit")
    print("Enter the key you wanna try")
    print("_"*20)

def show_keys_public(CA_serveur):
    addr_list = CA_serveur.addr_list
    addr_list_temp =[]
    for i in addr_list:
        addr_list_temp.append(re.findall('(?!/)\w*(?=.sock)',i)[0])
    print(addr_list_temp)
    return addr_list_temp

def send_keys_public(CA_serveur):
    entre = input("Entrez le name que vous souhaitez envoyer sa clé :")
    while entre not in show_keys_public(CA_serveur):
        entre = input("Entrez le name qui existe :")
        if entre =='q':
            print("quitter")
            return
    if CA_serveur.obtenir_keys_public(entre):
        print("Clé publique trouvée")
        if CA_serveur.send_keys_public_CA(entre):
            print("succès")
        else:
            print("échec")
    else:
        print("Aucune clé publique trouvée")

def main():
    CA_serveur = CA()
    pid = os.fork()
    if pid == 0:
        CA_serveur.communication.recv()
    else:
        display()
        while True:
            c = input(">>>")
            if c=='1':
                show_keys_public(CA_serveur)
            if c=='2':
                send_keys_public(CA_serveur)
            if c=='q':
                sys.exit(0)
            display()

if __name__ =='__main__':
    main()
