#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@File : tp2_affaire_outil.py
#@auteur : Junxi ZHANG
#@date : 30/10/2020
#@description : Affaire avec RSA


import random
import os
import math
import pickle
import hashlib

from tp2_decoration import Detection


#class Miller_Rabin
class Miller_Rabin(object):
    """Test de primalité de Miller-Rabin."""

    def __init__(self):
        super().__init__()

    @Detection.valeur_alerte('b < m','e > 0')
    @Detection.type_alerte(b = int,e = int,m = int)
    def fast_mod(self,b, e, m):
        """La méthode appelée exponentiation rapide. elle peut être remplacé par la méthode pow(b,e,m) de python3.
        Les propriétés algébriques de congruence sur les entier utilisées sont comme suit:
        (a * b) % c = (a % c) * (b % c) % c
        ab % c = (a % c)b % c

        L'analyse de cette méthode:
        Tout d'abord il faut convertir l'exposant e en notation binaire, avec n la longueur de e, e_i peut prendre la valeur 0 ou 1 pour tout i tel que 0 ≤ i < n - 1.
        e = e_0 * 2**0 + e_1 * 2**1 + e_2 * 2**2 + e_3 * 2**3 + ...... + e_(n-1) * 2**(n-1)
        a**e = a**(e_0 * 2**0) * a**(e_1 * 2**1) * a**(e_2 * 2**2) * a**(e_3 * 2**3) * ...... * a**(e_(n-1) * 2**(n-1))
        a**2**n=a**2**(n-1)**2
        donc a**(e_i*2**i)%m = base**2%m, avec base le module calculé au i-1e bit,


        Parameters
        ----------
        b : int
            Nombre base.
        e : int
            Nombre puissance.
        m : int
            Nombre diviseur.

        Returns
        -------
        int
            Nombre reste.

        """

        #result : Nombre reste.
        result = 1

        #base : la valeur par defaut est la valeur de l'unité sous binaire du nombre puissant，c'est-à-dire, base = b**(e_i*2**i)%m où i == 0，e_0 est inévitable égal à 1, car b est inévitable impair s'il a un reste.
        base = b


        while e > 0:

            #vérifier si le dernier bit actuel est 1.
            if e & 1 :
                result = (result * base) % m
            base = (base * base) % m

            #déplacer e pour détecter le prochain bit haut.
            e >>= 1

        return result

    @Detection.valeur_alerte('n % 2 != 0')
    @Detection.valeur_alerte('n > 0')
    @Detection.type_alerte(n = int)
    def is_premier(self,n):
        """Déterminer si n est premier par la méthode de Miller-Rabin.
        Les formules sont comme suit:
        n-1 = 2**k*d
        a = [1,n-1], r = [0,k-1]
        a**(2**r*d)%n == -1
        a**(2**r*d)%n = (a**d%n)**2**r%n = a**d%n == 1
        b = a%n, a**2%n == (a%n)**2%n -> a**2%n == b**2%n

        Parameters
        ----------
        n : int
            Nombre testé.

        Returns
        -------
        bool
            Si n s'agit d'un nombre premier, renvoie True, sinon False.

        """

        m = n - 1
        k = 0

        #lorsque m % 2 != 0, m est égal à d.
        while m % 2 == 0:
            m //= 2
            k += 1

        for _ in range(0,6): #réquence de tests, pour la précision. range = 6 par défaut, pour garantir la probabilité d'erreur minimale.

            is_premier = False
            a = random.randint(1, n - 1)

            #il peut être remplacé par pow(a, m, n).
            b = self.fast_mod(a, m, n)

            if b == 1:
                is_premier = True
            for _ in range(0, k):
                if b == n - 1:
                    is_premier = True
                    break
                b = (b * b) % n
            if not is_premier:
                return False
        return True

    @property
    def premier_list_10000(self):
        """Liste des nombres premiers inférieurs à 10000.

        Returns
        -------
        list
            List des nombres premiers inférieurs à 10000.

        """

        if not os.path.exists('premier_list_10000.txt'):
            with open('premier_list_10000.txt', mode='w', encoding='utf-8') as file:
                file.write('[1,2')
                number = 3
                while(number < 10000):
                    if self.is_premier(number):
                        file.write(','+str(number))
                    number+=2
                file.write(']')
        with open('premier_list_10000.txt', mode='r', encoding='utf-8') as file:
            return eval(file.read())

    @Detection.valeur_alerte('valeur_min < valeur_max and valeur_min > 0')
    @Detection.type_alerte(valeur_max = int,valeur_min = int)
    def premier_generateur(self,valeur_max,valeur_min):
        """Générateur du nombre premier.

        Parameters
        ----------
        valeur_min : int
            Limite minimale du nombre premier.
        valeur_max : int
            Limite maximale du nombre premier.

        Returns
        -------
        int
            Un nombre premier aléatoire.

        """

        while True:
            n = random.randint(valeur_min,valeur_max)
            if n % 2 == 0:
                n += 1

            #Améliorer l'efficacité
            for premier_10000 in self.premier_list_10000:
                if n % premier_10000 == 0:
                    continue

            if self.is_premier(n):
                return n


#class Myrsakey
class Myrsakey(object):
    """Le générateur qui utilise l'algorithme RSA."""

    def __init__(self, Miller_Rabin, keys_autre = dict()):

        #__key_length : la longueur du key binaire.
        self.__key_length = 1024

        self.Miller_Rabin = Miller_Rabin

        #Facteurs du RSA
        self.p = 0
        self.q = 0
        self.d = 0
        self.m = 0

        if len(keys_autre) == 0:
            self.n = 0
            self.e = 0
        else:
            self.n = keys_autre['n']
            self.e = keys_autre['e']

        super().__init__()


    @property
    def key_length(self):
        return self.__key_length

    @key_length.setter
    @Detection.valeur_alerte('key_length >= 128 and key_length <= 3072')
    @Detection.type_alerte(key_length = int)
    def key_length(self,key_length):
        self.__key_length = key_length

    def _initialisation_p_et_q(self):

        #*_length_d : la longueur du key décimal.
        key_length_d = len(str(pow(2,self.key_length)))
        p_length_d = random.randint(5,key_length_d - 5)
        q_length_d = key_length_d - p_length_d

        p_max = pow(10,p_length_d)
        p_min = pow(10,p_length_d-1)
        self.p = self.Miller_Rabin.premier_generateur(p_max,p_min)

        q_max = pow(10,q_length_d)
        q_min = pow(10,q_length_d-1)
        self.q = self.Miller_Rabin.premier_generateur(q_max,q_min)

    @property
    def _parametre_n(self):
        if self.n == 0:
            if self.q == 0 or self.p == 0:
                self._initialisation_p_et_q()
            self.n = (self.q)*(self.p)
        return self.n

    @property
    def _indicatrice_euler(self):
        if self.m == 0:
            if self.q == 0 or self.p == 0:
                self._initialisation_p_et_q()
            self.m = (self.q-1)*(self.p-1)
        return self.m

    @property
    def _parametre_e(self):
        if self.e == 0:
            if self.m == 0:
                self.m = self._indicatrice_euler
            while True:
                e_temp = random.randint(2,self.m-1)
                if math.gcd(e_temp,self.m) == 1:
                    self.e = e_temp
                    break
        return self.e

    @property
    def _parametre_d(self):
        if self.d == 0:
            if self.e == 0:
                self.e = self._parametre_e
            if self.m == 0:
                self.m = self._indicatrice_euler
            while True:
                if not pow(self.e,-1,self.m):
                    self.e = self._parametre_e
                else:
                    self.d = pow(self.e,-1,self.m)
                    break
        return self.d

    def key_montrer(self,key):
        """Key s’affiche en caractères."""

        strkey = ""
        str_temp_n = self.convertir_key(key['n'])
        if "e" in key:
            strkey = "keys_public = " + str_temp_n
            str_temp_e = self.convertir_key(key['e'])
            strkey += str_temp_e
        else:
            strkey = "keys_privee = " + str_temp_n
            str_temp_d = self.convertir_key(key['d'])
            strkey += str_temp_d
        print(strkey)

    def convertir_key(self,key):
        """Nombre s’affiche en caractères."""
        key_temp =''
        keys = [str(key)[i:i+2] for i in range(0,len(str(key)),2)]
        for i in keys:
            key_temp += chr(int(i)+24)
        return key_temp

    @property
    def keys_public(self):
        """Keys public du RSA.

        Returns
        -------
        dict
            Utiliser un dict car ses éléments ne peuvent pas être modifiés.

        """

        return ({'n':self._parametre_n,'e':self._parametre_e})

    @property
    def keys_privee(self):
        """Keys privee du RSA.

        Returns
        -------
        dict
            Utiliser un dict car ses éléments ne peuvent pas être modifiés.

        """

        return ({'n':self._parametre_n,'d':self._parametre_d})

    @Detection.type_alerte(a = int)
    def encrypt_int(self,a):
        """Chiffrement de l'int.

        Parameters
        ----------
        a : int
            Entier doit être chiffré.

        Returns
        -------
        int
            Entier chiffré.

        """

        return pow(a,self.keys_public['e'],self.keys_public['n'])

    @Detection.type_alerte(a = int)
    def decrypt_int(self,a):
        """Déchiffrement de l'int.

        Parameters
        ----------
        a : int
            Entier doit être chiffré.

        Returns
        -------
        int
            Entier déchiffré.

        """
        return pow(a,self.keys_privee['d'],self.keys_privee['n'])

    def _encrypt_data(self,datas):
        """Chiffrement le list de int.

        Parameters
        ----------
        datas : list
            List de str.

        Returns
        -------
        list
            List de int.

        """

        t = False
        e_data = []
        for data in datas:
            if data[0] == "0":
                t = True
            data_temp = str(self.encrypt_int(int(data)))
            if t:
                data_temp = '0'+ data_temp
            e_data.append(data_temp)
        return e_data

    def _decrypt_data(self,datas):
        """Déchiffrement le list de int.

        Parameters
        ----------
        datas : list
            List de int.

        Returns
        -------
        list
            List de int.

        """

        t = False
        d_data = []
        for data in datas:
            if data[0] == "0":
                t = True
            data_temp = str(self.decrypt_int(int(data)))
            if t:
                data_temp = '0'+ data_temp
            d_data.append(data_temp)

        return d_data

    def _binaire_decimal(self,data):
        """Binaire à décimal."""

        data_d = int.from_bytes(data,byteorder='big')
        return data_d

    def _decimal_binaire(self,datas):
        """Décimal à binaire."""

        datas_b = int(datas).to_bytes(308,byteorder='big')
        datas_b = datas_b.lstrip(b'\x00')
        return datas_b

    def _desassemblage_data(self,data):
        """Démonter le data int pour qu'il puisse être traité.

        Parameters
        ----------
        data : int
            Le data int.

        Returns
        -------
        list
            List de str.

        """

        datas = [str(data)[i:i+308] for i in range(0,len(str(data)),308)]
        return datas

    def _assemblage_data(self,datas):
        """Monter les datas binaires pour qu'ils puissent être traités.

        Parameters
        ----------
        datas : list
            List de int.

        Returns
        -------
        str
            Le data str.

        """

        data = ''
        for data_temp in datas:
            data += str(data_temp)
        return data

    @Detection.type_exclure_alerte(obj = bytes)
    def emballer_object(self,obj):
        """Traiter l'object en convertissant en data binaire.

        Parameters
        ----------
        obj : object
            L'object pour l'affaire.

        Returns
        -------
        bytes
            Le data binaire.

        """

        return pickle.dumps(obj)

    @Detection.type_alerte(data = bytes)
    def deballer_object(self,data):
        """Restaurer le data à partir des données binaires.

        Parameters
        ----------
        data : bytes
            Le data pour pouvoir être lu.

        Returns
        -------
        object
            L'object original.

        """

        return pickle.loads(data)

    def _pre_affaire_e(self,obj):
        """Processus avant de l'affaire."""

        obj_original = self._binaire_decimal(obj)
        datas_affaire = self._desassemblage_data(obj_original)
        return datas_affaire

    def _fin_affaire_d(self,datas):
        """Processus après de l'affaire."""

        obj_affaire_t = self._assemblage_data(datas)
        obj_affaire = self._decimal_binaire(obj_affaire_t)
        return obj_affaire

    @Detection.type_alerte(obj = bytes)
    def encrypt_affaire_c(self,obj):
        """Processus de cryptage de key public."""

        datas_affaire = self._pre_affaire_e(obj)
        datas_affaire_e = self._decrypt_data(datas_affaire)
        return self.emballer_object(datas_affaire_e)

    @Detection.type_alerte(obj = bytes)
    def decrypt_affaire_c(self,obj):
        """Processus de décryptage de key public."""

        datas_affaire = self.deballer_object(obj)
        datas_affaire_de = self._encrypt_data(datas_affaire)
        return self._fin_affaire_d(datas_affaire_de)

    @Detection.type_alerte(obj = bytes)
    def encrypt_affaire_o(self,obj):
        """Processus de cryptage de l'object."""

        datas_affaire = self._pre_affaire_e(obj)
        datas_affaire_e = self._encrypt_data(datas_affaire)
        return self.emballer_object(datas_affaire_e)

    @Detection.type_alerte(obj = bytes)
    def decrypt_affaire_o(self,obj):
        """Processus de décryptage de l'object."""

        datas_affaire = self.deballer_object(obj)
        datas_affaire_de = self._decrypt_data(datas_affaire)
        return self._fin_affaire_d(datas_affaire_de)


#class Signature_N
class Signature_N(object):
    """Signature numérique."""

    def __init__(self,Myrsakey):
        self.Myrsakey = Myrsakey
        super().__init__()

    @Detection.type_alerte(obj = bytes)
    def _digest(self,obj):
        return hashlib.blake2b(obj).hexdigest()

    @Detection.type_alerte(obj = bytes)
    def _paquet_signature(self,obj):
        obj_temp = self.Myrsakey.emballer_object(self._digest(obj))
        return self.Myrsakey.encrypt_affaire_c(obj_temp)

    @Detection.type_alerte(obj = bytes)
    def _paquet_obj(self,obj,keys_autre):
        a_temp = Myrsakey(Miller_Rabin(),keys_autre)
        return a_temp.encrypt_affaire_o(obj)

    @Detection.type_exclure_alerte(obj = bytes)
    def paquet_affaire(self,obj,keys_autre):
        obj_temp = self.Myrsakey.emballer_object(obj)
        o_t = {'s_n':self._paquet_signature(obj_temp),'data_obj':self._paquet_obj(obj_temp,keys_autre)}
        return self.Myrsakey.emballer_object(o_t)

    @Detection.type_alerte(obj = bytes)
    def _depaquet_signature(self,obj,keys_autre):
        a_temp = Myrsakey(Miller_Rabin(),keys_autre)
        obj_temp = a_temp.decrypt_affaire_c(obj)
        return self.Myrsakey.deballer_object(obj_temp)

    @Detection.type_alerte(obj = bytes)
    def _depaquet_obj(self,obj):
        return self.Myrsakey.decrypt_affaire_o(obj)


    @Detection.type_alerte(obj = bytes)
    def depaquet_affaire(self,obj,keys_autre):
        obj_temp = self.Myrsakey.deballer_object(obj)
        return self._depaquet_obj(obj_temp['data_obj']),self._depaquet_signature(obj_temp['s_n'],keys_autre)

    def _comparaison_digest(self,obj,digest):
        if self._digest(obj) == digest:
            return True
        else:
            return False

    def lire_object(self,obj,digest):
        if self._comparaison_digest(obj,digest):
            return self.Myrsakey.deballer_object(obj)
        else:
            return False
