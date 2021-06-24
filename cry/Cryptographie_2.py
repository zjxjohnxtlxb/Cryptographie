#@Cryptographie_2
#@auteur : Junxi ZHANG
#@date : 09/10/2020
#@description :  Chiffrement par décalage ... le retour ! et cryptanalyse

#import Cryptographie_1 pour l'alphalist et des fonctions.
import Cryptographie_1

#import re pour le regular expression operations.
import re

import collections

#frequence des lettres，les données proviennent de https://fr.wikipedia.org/wiki/Analyse_fréquentielle
frequence_theorique = [9.42,1.02,2.64,3.39,15.87,0.95,1.04,0.77,8.41,0.89,0.00,5.34,3.24,7.15,5.14,2.86,1.06,6.46,7.90,7.26,6.24,2.15,0.00,0.30,0.24,0.32]

filefin = "_de.txt"
strlambda = "[^a-z]"

#Retour 1
#textToVig(text,key,alphalist)
def textToVig(text,key,alphalist):
    """chiffre le texte text, selon la méthode de Vigenere.

    Parameters
    ----------
    text : string
        le texte text que l'on traite.
    key : tableau
        la cle de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    string
        le texte texte chiffré.

    """

    #l : la longueur de la cle.
    l = len(key)

    #indexcle : index de cle actuelle.
    indexcle = 0

    #textres : le texte chiffré.
    textres = ''

    #chiffrer le text avec la méthode de Vigenere.

    text = Cryptographie_1.clean(text)
    text = re.sub(strlambda,'',text)
    for i, nums in enumerate(text):
        indexcle = i % l
        textres += Cryptographie_1.charToCesar(nums,key[indexcle],alphalist)
    return textres

"""test_code pour textToVig(text,key,alphalist)

print(textToVig("objectif",[1, 3, 2],Cryptographie_1.alphalist))

"""

#vigToText(text,key,alphalist)
def vigToText(text,key,alphalist):
    """déchiffre le texte text, selon la méthode de Vigenere.

    Parameters
    ----------
    text : string
        le texte text que l'on traite.
    key : tableau
        la cle de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    string
        le texte texte déchiffré.

    """

    #l : la longueur de la cle.
    l = len(key)

    #indexcle : index de cle actuelle.
    indexcle = 0

    #textres : le texte déchiffré.
    textres = ''

    #déchiffrer le text avec la méthode de Vigenere.
    for i, nums in enumerate(text):
        indexcle = i % l
        textres += Cryptographie_1.cesarToChar(nums,key[indexcle],alphalist)
    return textres

"""test_code pour vigToText(text,key,alphalist)

print(vigToText("pelffvji",[1, 3, 2],Cryptographie_1.alphalist))

"""

#Retour 2
#fileToVig(filename,key,alphalist)
def fileToVig(filename,key,alphalist):
    """chiffre le texte qui se trouve dans le fichier.

    Parameters
    ----------
    filename : string
        name du fichier.
    key : tableau
        la cle de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    none

    """

    #file_context : le contenu du fichier
    file_context = Cryptographie_1.openFile(filename)

    #file_hash : le texte chiffré.
    file_hash = textToVig(file_context,key,alphalist)

    #créer un fichier chiffré.
    filenamearr = filename.split('.')
    Cryptographie_1.writeFile(filenamearr[0]+"_code.txt",file_hash)

"""test_code pour textToCesar(text,key,alphalist)

fileToVig("test.txt",[1, 3, 2],Cryptographie_1.alphalist)

"""

#vigToFile(filename,key,alphalist)
def vigToFile(filename,key,alphalist):
    """déchiffre le texte qui se trouve dans le fichier.

    Parameters
    ----------
    filename : string
        name du fichier.
    key : tableau
        la cle de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    none

    """

    #file_context : contenu du fichier.
    file_context = Cryptographie_1.openFile(filename)

    #file_dehash : le texte déchiffré.
    file_dehash = vigToText(file_context,key,alphalist)

    #créer un fichier déchiffré.
    filenamearr = filename.split('_')
    Cryptographie_1.writeFile(filenamearr[0]+"_decode.txt",file_dehash)

"""test_code pour vigToFile(text,key,alphalist)

vigToFile("test_code.txt",[1, 3, 2],Cryptographie_1.alphalist)

"""

#Cryptanalyse
#Attaque par brute force semi-automatique
#attaque_brute_force_sa(text,alphalist)
def attaque_brute_force_sa(text,alphalist):
    """trouve le cle pour le texte texte chiffré.

    Parameters
    ----------
    text : string
        un texte texte chiffré.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    none

    """

    #strcontinuer : la chaine texte d'indication.
    strcontinuer = "Pour tester la cle suivante, appuyer sur la touche N, sinon S pour stopper."

    #key : la cle pour chiffrer.
    key = 1

    #textres : le texte déchiffré.
    textres = ''

    #le tableau pour les 40 premiers caractères du texte déchiffré.
    textbuffer = ['']*40

    #in_content : commande entrée par usager
    in_content = ''

    while (True):

        #obtenir les 40 premiers caractères du texte déchiffré basé sur la cle actuelle
        textres = Cryptographie_1.cesarToText(text,key,Cryptographie_1.alphalist)
        for i, buffe in enumerate(textres):
            if i < 40:
                textbuffer[i] = buffe
        print("cle ",key," - Texte : ",''.join(textbuffer))

        #demander à l’utilisateur s’il faut s’arrêter ou continuer.
        in_content = input(strcontinuer)
        if in_content.lower() == 'n':

            #augmenter automatiquement la valeur de cle à chaque cycle
            key += 1
        elif in_content.lower() == 's':
            break
        else:
            continue

"""test_code pour vigToFile(text,key,alphalist)

C = Cryptographie_1.textToCesar("bonjour à toutes et à tous, soyez les bienvenues",3,Cryptographie_1.alphalist)
print(C)
attaque_brute_force_sa(C,Cryptographie_1.alphalist)

"""

#Attaque statistique sur le « e »
#e_attack(text,alphalist)
def e_attack(text,alphalist):
    """déchiffre le texte avec la méthode d’attaque sur « e ».

    Parameters
    ----------
    text : string
        un texte texte chiffré.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).


    Returns
    -------
    none

    """

    #strcontinuer : la chaine texte d'indication.
    strcontinuer = "Pour stopper la cle suivante, appuyer sur la touche S, sinon autre touche pour continuer."

    #key : la cle pour chiffrer.
    key = 0

    #après_décalage : le index de lettre la plus fréquente.
    aprdecalage = 0

    #textres : le texte déchiffré.
    textres = ''

    #in_content : commande entrée par usager
    in_content = ''

    #obtenir le nombre d'occurrences de chaque lettre，chiffre : un tableau pour l'occurence.
    chiffre = Cryptographie_1.occurenceOfLetter(text,Cryptographie_1.alphalist)

    while (True):

        #contrôle d'attaque efficace
        if max(chiffre) != 0:
            aprdecalage = chiffre.index(max(chiffre))
        else:
            print ("Toutes les possibilités ont été essayées, l'attaque est terminée.")
            break

        #éviter la répétition de la valeur maximale, impossible d'en récupérer une autre
        chiffre[aprdecalage] = 0
        key = aprdecalage - Cryptographie_1.alphalist.index('e')
        if key < 0:
            key += len(Cryptographie_1.alphalist)

        #obtenir les caractères du texte déchiffré basé sur la cle actuelle
        textres = Cryptographie_1.cesarToText(text,key,Cryptographie_1.alphalist)
        print("cle ",key," - Texte : ",''.join(textres))

        #demander à l’utilisateur s’il faut s’arrêter ou continuer.
        in_content = input(strcontinuer)
        if in_content.lower() == 's':
            break

"""test_code pour e_attack(text,alphalist)

e_attack("fsrnsyv e xsyxiw ix e xsyw wscid piw fmirziryiwbbbbbbbbbbbbbbbbbbbbbbbbbbbb",Cryptographie_1.alphalist)

"""

#Attaque par coïncidence 1
#indexC(text,alphalist)
def indexC(text,alphalist):
    """une fonction qui utilise la fonction occurenceOfLetter() qui détermine l’indice de coïncidence du texte text et le retourne.

    Parameters
    ----------
    text : string
        un texte texte chiffré.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    ic : float
        l’indice de coïncidence du texte text.

    """

    #le prétraitement du texte text.
    text = Cryptographie_1.clean(text)

    #chiffre : un tableau pour l'occurence.
    chiffre = Cryptographie_1.occurenceOfLetter(text, Cryptographie_1.alphalist)

    #ic ：l’indice de coïncidence du texte text.(qui est la probabilité que deux lettres choisies aléatoirement dans un texte soient identiques.)
    #la formule mathématique pour ic_lm ic de chaque lettre est: ic_lm = (n_lm*(n_lm - 1))/(n*(n-1)),avec n le nombre de lettres total du texte, n_lm le nombre de quelconque lettre choisi aléatoirement deux fois.
    #ic est la somme de toutes les possibilités.
    #fonction somme : simplifier le code.
    somme = lambda n : n * (n - 1)
    ic_lm,ic  = [],0.0
    text_ic = re.sub(strlambda,'',text)
    n = len(text_ic)
    for i, n_lm in enumerate(chiffre):
        ic_lm.append(somme(n_lm))
    ic = sum(ic_lm)/somme(n)
    return ic

"""test_code pour indexC(text,alphalist)

ic = indexC("Differential Privacy is the state-of-the-art goal for the problem of privacy-preserving data release and privacy-preserving data mining. Existing techniques using differential privacy, however, cannot effectively handle the publication of high-dimensional data. In particular, when the input dataset contains a large number of attributes, existing methods incur higher computing complexity and lower information to noise ratio, which renders the published data next to useless. This proposal aims to reduce computing complexity and signal to noise ratio. The starting point is to approximate the full distribution of high-dimensional dataset with a set of low-dimensional marginal distributions via optimizing score function and reducing sensitivity, in which generation of noisy conditional distributions with differential privacy is computed in a set of low-dimensional subspaces, and then, the sample tuples from the noisy approximation distribution are used to generate and release the synthetic dataset. Some crucial science problems would be investigated below: (i) constructing a low k-degree Bayesian network over the high-dimensional dataset via exponential mechanism in differential privacy, where the score function is optimized to reduce the sensitivity using mutual information, equivalence classes in maximum joint distribution and dynamic programming; (ii)studying the algorithm to compute a set of noisy conditional distributions from joint distributions in the subspace of Bayesian network, via the Laplace mechanism of differential privacy. (iii)exploring how to generate synthetic data from the differentially private Bayesian network and conditional distributions, without explicitly materializing the noisy global distribution. The proposed solution may have theoretical and technical significance for synthetic data generation with differential privacy on business prospects.",Cryptographie_1.alphalist)
print(ic)

"""

#Attaque par coïncidence 2
#découpure(s_test):
def decoupure(text,l):
    """découper text en sous-textes par la même cle cesar.

    Parameters
    ----------
    text : string
        un texte texte chiffré.
    l : int
        la longueur estimée de la cle.

    Returns
    -------
    list
        le list de sous-textes decoupés par la même cle cesar.

    """

    #le prétraitement du texte text.
    text = Cryptographie_1.clean(text)
    text = re.sub(strlambda,'',text)
    textbuffer = []
    for i in range(l):
        textbuffer.append(text[i::l])
    return textbuffer

#key_len(...)
def key_len(text,alphalist,ic_lg =  0.0778):
    """une fonction retourne la longueur estimée de la cle.

    Parameters
    ----------
    text : string
        un texte texte chiffré.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).
    ic_lg : float
        l’indice de coïncidence de la langue analysée. La valeur pour défaut est 0.0778 pour le français.

    Returns
    -------
    int
        la longueur estimée de la cle.

    """

    #le prétraitement du texte text.
    textbuffer = []
    text = Cryptographie_1.clean(text)
    text = re.sub(strlambda,'',text)

    #ic_m : la moyenne d'ic estimé. L'ic d'text comme valeur par défaut
    ic_m = indexC(text,alphalist)

    #l_p : la longueur possible de la cle avec son ic, l_ic.
    l_p,l_ic = [0]*3,[0]*3

    #l : la longueur estimée de la cle.
    l = 1

    #ics : le list d'ic pour le texte par la longueur estimée de la cle l.
    ics = []
    for k in range(3):
        while ic_lg-0.005>ic_m:
            l += 1
            textbuffer = decoupure(text,l)
            if len(textbuffer) != 1:
                for i in textbuffer:
                    ics.append(indexC(i,alphalist))
                ic_m = sum(ics)/l
            else:
                break
            ics.clear()
        l_p[k],l_ic[k]=l,ic_m
        ic_m = 0
    for i in range(3):
        for j in l_p[i:]:
            if j % l_p[i] == 0:
                return l_p[i]
    return l_p[l_ic.index(max(l_ic))]

"""test_code pour key_len(text,alphalist,ic_lg =  0.0778)

print(key_len("lvktwvgvgnodttqifqqmubujglevmbkhziczglcsphweyvwttwoqseshxenjsgaxejgwvxqalrsxczrqsswgiaidjmxipddjiumeawfkfigfaarkvtjlawvqalhwgjvvviwwwavsuvmhnrwsfxkiyufazcklmcoixmehofrqbrktwgvqijzqlcvqqsllgxhgzagcbvtbgjjqtmraqgvfncfenlnyoarrieywuyniebvwrvprnbhyvlnyokivkbshsmpanqojkgvhrpwvqnnyhjmdcgjgwbkagnbyqgbutrkmpkhwvakjmehcetwbvsuusoxyjlaxaiaizgagzvstgvoigncfxqvbngwvcbvtkzmepejbvitagmshydtvxvwhfigfbwbvbbzgwpgafyvawrzbuckenivrglstmqzqwgquczharikbrddizqgdofhuqtsodxqvbngwvcbvthziubnwharixbnblmubbfdhvqfvrolivprkidpfqfyfafwbvtbgjjqtmraqgvfncfenlnyokivevyvswgbbkzgafqzjbkmqvnqasviqafzvmubenpmxkwaxjaeqxgnaadkvtxqgvgnhsqlmqvnsrjifcpnbywgvfnhazkblnbolkkulsfitigncfshvbngqgqvqnhaspiyiwkxtqozhaspajnhzhknsjfwrvqnqdjmxipdwkgquczhwhkvnxslshtbbraqgvfncfenahggheemffbvxjmayvwwcucqslyrtrxtjsobujbgmugnudjszqzfhasplvxhjmdcgncfetmhxsvxqorssjevmnsrjinmnxsllgalshzivqpioleumgxceiezhhwspukvjbuirzbgzwquebzzvfgqaaskxkonysvfgtbbwuspagwiuxkvtfzgamlrlfwidiljgaepvrykgvmwijfllgpvlvvmomaxwgrctqfhswgbinowbrwajblmctzjqzepqfrwfhknsjfwrvqnqdjmxipdkzitmgmskgqzrkifgvqbswksrbvrwrifbbwsvyemgmskipavywnmvghxwfkocgzodmpnbwasxkwajemmxiyjbuietnxgwwkvzflaqwuwtwfxfqfyfafwbvtbsrfllsoemexetujeouvsuamubhimaribujodkqzvyvexqkbrdmxgifjhgjpwvxmusplvywgrctqnglvkjhywgrunetabskvgiwkxtqozhaspavshziucoxdsggwsgoqiuqnsbwxywepjaevprqohpckrrsulcvvxagjfqsksjipbvfzhvkdnhmamkmkuzgvkvtmcoxqorssjevmfdbllgbvhrsxcnetallglvktwvgvgnodpaxenjsxgjndskmcvajhostsnsrusplvywgrctqnglvkjhywgruevyvgyvmkuzagkbydasxgzvfzadkvtyvwrqqfdudsdiyiwkxtqozhaspbujdjsrwfjrksncgncfqcgufjwxjmbwslmeiyfbvxgkuswuenavlbajkknsqwjqzfdbllgbvhrsxcorssjevqbskaxjlvktwvgvgnodttqifqqspjhxwfiuacwcktgkgxvzlj",Cryptographie_1.alphalist,0.065))

"""

#Attaque par coïncidence 3
#indexNC(text,key,alphalist)
def indexNC(text,key,alphalist):
    """une fonction qui détermine l’indice de coïncidence du texte text chiffré par le cesar de clef key et le retourne.

    Parameters
    ----------
    text : string
        un texte texte chiffré.
    key : int
        la valeur de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    float
        l’indice de coïncidence du texte text par le cesar de clef key.

    """

    #textres : le texte chiffré par le cesar de clef key
    textres = Cryptographie_1.cesarToText(text,key,alphalist)
    #frequence : un tableau pour la frequence de lettres du textres.
    frequence = Cryptographie_1.rateOfLetter(textres,alphalist)

    #la formule mathématique pour nic est: nic = sum(frequence[lm]*frequence_theorique[lm]) for lm in alphalist, avec lm le nombre de quelconque lettre choisi aléatoirement deux fois.
    nic = 0
    for i, nums in enumerate(frequence_theorique):
        nic += abs(frequence[i]-nums)
    return nic

#calculer_cesar (text,alphalist):
def calculer_cesar(text,alphalist):
    """calculer la cle cesar et le retourne.

    Parameters
    ----------
    text : string
        un texte texte chiffré.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    int
        la cle cesar utilisée.

    """

    #nics ： un list pour tous nics obtenus
    nics = []

    for i in range(26):
        nics.append(indexNC(text,i,alphalist))
    return nics.index(min(nics))

#decode(filename, ...)
def decode(filename,alphalist,ic_lg =  0.0778):
    """une fonction déchiffre le texte du fichier filename.

    Parameters
    ----------
    filename : string
        name du fichier.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).
    ic_lg : float
        l’indice de coïncidence de la langue analysée. La valeur pour défaut est 0.0778 pour le français.

    Returns
    -------
    none

    """

    #file_context : contenu du fichier.
    file_context = Cryptographie_1.openFile(filename)
    file_context = Cryptographie_1.clean(file_context)

    #obtenir l la longueur estimée de la cle.
    l= key_len(file_context,alphalist,ic_lg)

    #la cle Vigenere
    cle =[0]*l

    #le prétraitement du texte.
    text_c = decoupure(file_context,l)
    for i, text_cs in enumerate(text_c):
        cle[i]= calculer_cesar(text_cs,alphalist)

    #initialiser les tableaux déchiffrés à utiliser
    textdehash = re.sub("[a-z]",'a',file_context)
    file_context = re.sub(strlambda,'',file_context)
    vig_dehash = vigToText(file_context,cle,alphalist)
    it = iter(vig_dehash)

    #l'empaquetage du texte déchiffré.
    file_dehash = ''
    for i, j in enumerate(textdehash):
        if j == 'a':
            file_dehash += next(it)
        else:
            file_dehash += j

    #créer un fichier déchiffré.
    filenamearr = filename.split('.')
    Cryptographie_1.writeFile(filenamearr[0]+filefin,file_dehash)

"""test_code pour decode(filename,alphalist,ic_lg =  0.0778)

decode("decode.txt",Cryptographie_1.alphalist)

"""

#Attaque par doublement de lettre en fin de mot 1
#doublelettre_cesarToText(text,alphalist)
def doublelettre_cesarToText(filename,alphalist):
    """un algorithme fiable qui permet de déchiffrer un texte chiffré par la méthode César sans la cle en se basant sur les doublements de lettre de fin de mots

    Parameters
    ----------
    filename : string
        name du fichier.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    none

    """

    #file_context : le contenu du fichier
    file_context = Cryptographie_1.openFile(filename)

    #le prétraitement du texte text.
    text = Cryptographie_1.clean(file_context)
    text_c = text.split(" ")
    buffe = ''
    text_mots = []
    desinence = []
    for i in text_c:
        buffe = re.sub(strlambda,"",i)
        if len(buffe) != 0:
            text_mots.append(buffe)

    #rechercher les doublements de lettre de fin de mots
    for i, mot in enumerate(text_mots):

        #le mot a des doublements de lettre à la fin souvent plus long que 3
        if len(mot) >= 4:
            if mot[-3] == mot[-2]:
                desinence.append(mot[-1])
            if mot[-4] == mot[-3]:
                desinence.append(mot[-2])

    #habituellement, dans ce cas, e est le plus à la fin. Trouver donc le cle cesar k via e.
    k =(ord(max(desinence, key = desinence.count))-ord('e'))%26

    #textres : le texte chiffré par le cesar de clef key
    textres = Cryptographie_1.cesarToText(text,k,alphalist)

    #créer un fichier déchiffré.
    filenamearr = filename.split('.')
    Cryptographie_1.writeFile(filenamearr[0]+filefin,textres)

"""test_code pour doublelettre_cesarToText(text,alphalist)

doublelettre_cesarToText("text_code.txt",Cryptographie_1.alphalist)

"""

#Attaque par doublement de lettre en fin de mot 2
#Compte tenu de la nécessité de trouver la fin de mot, il doit y avoir des phrases significatifs et des espaces obligatoires.
#doublelettre_vigToText(text,alphalist)
def doublelettre_vigToText(filename,alphalist,ic_lg =  0.0778):
    """un algorithme fiable qui permet de déchiffrer un texte chiffré par la méthode Vigenere sans la cle en se basant sur les doublements de lettre de fin de mots

    Parameters
    ----------
    filename : string
        name du fichier.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).
    ic_lg : float
        l’indice de coïncidence de la langue analysée. La valeur pour défaut est 0.0778 pour le français.

    Returns
    -------
    none

    """

    #file_context : le contenu du fichier
    file_context = Cryptographie_1.openFile(filename)
    file_context = Cryptographie_1.clean(file_context)

    #obtenir l la longueur estimée de la cle.
    l= key_len(file_context,alphalist,ic_lg)

    #la cle Vigenere
    cle =[0]*l

    #le prétraitement du texte.
    text_c = decoupure(file_context,l)
    textdehash = re.sub("[a-z]",'a',file_context)
    text_m = file_context.split(" ")
    buffe = ''
    text_mots = []
    desinence = []
    desinencebuffer = [[] for i in range(l)]
    desinence_e =[]
    desinence_cle =[]

    for i in text_m:
        buffe = re.sub(strlambda,"",i)
        if len(buffe) != 0:
            text_mots.append(buffe)

    #rechercher les doublements de lettre de fin de mots
    index_textm = 0
    for i, mot in enumerate(text_mots):
        #le mot a des doublements de lettre à la fin souvent plus long que 3
        if len(mot) >= 4:
            desinence.append([index_textm+len(mot)-2,mot[-2]])
            desinence.append([index_textm+len(mot)-1,mot[-1]])
        index_textm += len(mot)

    #rechercher la cle possible.
    #la relation entre l'indice de segmentation et l'ancien indice de la même lettre est : ancien = numéro de segmentation + l'indice de segmentation * longueur de cle
    for i, j in enumerate(desinencebuffer):
        for k in desinence:
            if k[0]%l == i:
                j.append(k[1])
    for i in desinencebuffer:
        desinence_e.append(list(dict(collections.Counter(i).most_common(2))))#Considérez ici en raison de l'existence de pluriel qui se termine par x ou s.
    for desinence_es in desinence_e:
        desinence_cle.append([(ord(i)-ord('e'))%26 for i in desinence_es])

    #obtenir l'indice exact du tableau de desinence_cle.
    clepossibles = []
    for i, clepossible in enumerate(desinence_cle):
        for j, c_p in enumerate(clepossible):
            clepossibles.append(indexNC(text_c[i],c_p,alphalist))
        cle[i] = clepossible[clepossibles.index(min(clepossibles))]
        clepossibles.clear()

    #initialiser les tableaux déchiffrés à utiliser
    file_context = re.sub(strlambda,'',file_context)
    vig_dehash = vigToText(file_context,cle,alphalist)
    it = iter(vig_dehash)

    #l'empaquetage du texte déchiffré.
    file_dehash = ''
    for i, j in enumerate(textdehash):
        if j == 'a':
            file_dehash += next(it)
        else:
            file_dehash += j

    #créer un fichier déchiffré.
    filenamearr = filename.split('.')
    Cryptographie_1.writeFile(filenamearr[0]+filefin,file_dehash)

"""test_code pour doublelettre_vigToText(filename,alphalist,ic_lg =  0.0778)

doublelettre_vigToText("textv_code.txt",Cryptographie_1.alphalist)

"""
