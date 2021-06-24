#@Cryptographie_1
#@auteur : Junxi ZHANG
#@date : 08/10/2020
#@description :  Prolegomenes et cesar

#Prolégomènes 1
#alphalist : une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).
alphalist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#Prolégomènes 2
#clean(text)
def clean(text):
    """une fonction qui prend en paramètre un texte et qui renvoie le texte text après avoir :
        a. Converti tout le texte en minuscule (voir la fonction lower())
        b. Remplacé les lettres accentuées par leurs équivalents sans accent. (voir la fonction replace())

    Parameters
    ----------
    text : string
        la chaîne de caractères que l'on traite.

    Returns
    -------
    string
        la chaîne que l'on demande.

    """

    #convertir tout le texte en minuscule.
    text = text.lower()

    #Remplacer les lettres accentuées par leurs équivalents sans accent.
    #rep_dic : un dictionaire pour replacer les lettres accentuées.
    rep_dic = {'à':'a','â':'a','ç':'c','é':'e','è':'e','ê':'e','ë':'e','î':'i','ï':'i','ô':'o','û':'u','ù':'u','ü':'u','ÿ':'y'}
    text = [rep_dic[i] if i in rep_dic else i for i in text]
    return ''.join(text)

"""test_code pour clean(text)

text = "Marïné"
text = clean(text)
print(text)

"""

#Prolégomènes 3
#occurenceOfLetter(text,alphalist)
def occurenceOfLetter(text,alphalist):
    """cette fonction renvoie une liste du nombre d’occurrence de chaque caractère dans la chaine texte.

    Parameters
    ----------
    text : string
        la chaîne de caractères que l'on traite.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    tableau<int>
        une liste du nombre d’occurrence de chaque caractère dans la chaine texte.

    """

    #chiffre : un tableau pour l'occurence.
    chiffre = [0]* len(alphalist)

    #compter le nombre d'occurrences de chaque lettre.
    text = clean(text)
    for i in alphalist:
        chiffre[alphalist.index(i)] = text.count(i)
    return chiffre

"""test_code pour occurenceOfLetter(text,alphalist)

text = "Marïné"
chiffre = occurenceOfLetter(text, alphalist)
print(chiffre)

"""

#Prolégomènes 4
#rateOfLetter(text,alphalist)
def rateOfLetter(text,alphalist):
    """renvoie une liste de la frequence (arrondi à 3 chiffres après la virgule) d’apparition de chaque lettre de notre liste alphalist dans la chaine texte.

    Parameters
    ----------
    text : string
        la chaîne de caractères que l'on traite.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    tableau<string>
        une tableau de la frequence de chaque caractère dans la chaine texte.

    """

    #obtenir le tableau de l'occurence.
    chiffre = occurenceOfLetter(text,alphalist)

    #frequence : un tableau pour la frequence.
    frequence =[]

    #l : la longueur de la chaîne.
    l = len(text)

    #compter le nombre de la frequence de chaque lettre.
    for i in chiffre:
        frequence.append(i/l*100)
    return frequence

"""test_code pour rateOfLetter(text,alphalist)

text = "Marïné"
frequence = rateOfLetter(text, alphalist)
print(frequence)

"""
#Prolégomènes 5
#openFile(filename)
def openFile(filename):
    """une fonction prend en paramètre le nom du fichier que l’on veut lire et qui renvoie le contenu de ce fichier sous forme de chaine de caractère.

    Parameters
    ----------
    filename : string
        name du fichier.

    Returns
    -------
    string
        contenu du fichier.

    """

    #file : le fichier que l'on traite.
    #ouvrir le fichier qui doit exister.
    file = open(filename,'r',encoding='utf-8')

    #obtenir le contenu du fichier
    file_context = file.read()

    #fermer le fichier
    file.close()
    return file_context

#Prolégomènes 6
#writeFile(filename)
def writeFile(filename,text):
    """une fonction prend en paramètre le nom du fichier dans lequel on veut écrire le contenu de la chaine de caractère.

    Parameters
    ----------
    filename : string
        name du fichier.
    text : string
        le contenu de la chaine de caractère.

    Returns
    -------
    none

    """
    #ouvrir le fichier, si il n'existe pas, on en crée un
    file = open(filename,'w',encoding='utf-8')

    #écrire le texte text dans le fichier.
    file.write(text)

    #fermer le fichier
    file.close()

"""test_code pour writeFile(filename,text) et openFile(filename)

writeFile("test.txt","objectif")
print(openFile("test.txt"))

"""

#Chiffrement par décalage 1
#charToCesar(char,key,alphalist)
def charToCesar(char,key,alphalist):
    """si le caractère n’est pas présent dans alphalist, alors la fonction retourne le caractère char passé en paramètre.

    Parameters
    ----------
    char : char
        le char que l'on traite.
    key : int
        la valeur de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).


    Returns
    -------
    char
        le char que l'on demande.

    """
    #le caractère n’est pas présent dans alphalist.
    if char not in alphalist:
        return char

    #le caractère est présent dans alphalist.
    #charindex : index de char dans l'alphalist.
    charindex = alphalist.index(char)+key
    if charindex >= len(alphalist):
        return alphalist[charindex - len(alphalist)]
    else:
        return alphalist[charindex]

"""test_code pour charToCesar(char,key,alphalist)

print(charToCesar('a',3,alphalist))
print(charToCesar('5',3,alphalist))
print(charToCesar('z',3,alphalist))

"""

#Chiffrement par décalage 2
#cesarToChar(char,key,alphalist)
def cesarToChar(char,key,alphalist):
    """qui fait l’inverse de la fonction charToCesar().

    Parameters
    ----------
    char : char
        le char que l'on traite.
    key : int
        la valeur de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    char
        le char que l'on demande.

    """

    #le caractère n’est pas présent dans alphalist.
    if char not in alphalist:
        return char

    #le caractère est présent dans alphalist.
    #charindex : index de char dans l'alphalist.
    charindex = alphalist.index(char)-key
    if charindex < 0:
        return alphalist[charindex + len(alphalist)]
    else:
        return alphalist[charindex]

"""test_code pour cesarToChar(char,key,alphalist)

cesarToChar ('d',3,alphalist)
cesarToChar ('5',3,alphalist)
cesarToChar ('c',3,alphalist)

"""

#Chiffrement par décalage 3
#textToCesar(text,key,alphalist)
def textToCesar(text,key,alphalist):
    """renvoie le texte chiffré.

    Parameters
    ----------
    text : string
        la chaine texte que l'on traite.
    key : int
        la valeur de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    string
        le texte chiffré.

    """

    #textres : le texte chiffré
    textres = ''

    #chiffrer le texte text.
    text = clean(text)
    for i in text:
        textres += charToCesar(i,key,alphalist)
    return textres

"""test_code pour textToCesar(text,key,alphalist)

textToCesar("le chiffrement de cesar est pas du tout secure",3,alphalist)

"""

#Chiffrement par décalage 4
#cesarToText(text,key,alphalist)
def cesarToText(text,key,alphalist):
    """qui fait l’inverse de la fonction textToCesar().

    Parameters
    ----------
    text : string
        la chaine texte que l'on traite.
    key : int
        la valeur de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    string
        le texte déchiffré.

    """

    #textres : le texte chiffré.
    textres = ''

    #déchiffrer le texte text.

    for i in text:
        textres += cesarToChar(i,key,alphalist)
    return textres

"""test_code pour textToCesar(text,key,alphalist)

cesarToText("oh fkliiuhphqw gh fhvdu hvw sdv gx wrxw vhfxuh",3,alphalist)

"""

#Chiffrement par décalage 5
#cesarTofile(filename,key,alphalist)
def fileToCesar(filename,key,alphalist):
    """envoie le contenu du fichier chiffré dans un fichier qui porte le nom de la variable filename suivi de _code.txt.

    Parameters
    ----------
    filename : string
        name du fichier.
    key : int
        la valeur de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    none

    """

    #file_context : contenu du fichier.
    file_context = openFile(filename)

    #file_hash : le texte chiffré.
    file_hash = textToCesar(file_context,key,alphalist)

    #créer un fichier chiffré.
    filenamearr = filename.split('.')
    writeFile(filenamearr[0]+"_code.txt",file_hash)

"""test_code pour fileToCesar(filename,key,alphalist)

fileToCesar("test.txt",3,alphalist)

"""

#Chiffrement par décalage 6
#cesarTofile(filename,key,alphalist)
def cesarTofile(filename,key,alphalist):
    """déchiffrer le fichier.

    Parameters
    ----------
    filename : string
        name du fichier.
    key : int
        la valeur de décalage.
    alphalist : tableau<string>
        une liste qui contient l’ensemble des lettres de l’alphabet française en minuscule sans les accents (de a à z).

    Returns
    -------
    none

    """

    #file_context : contenu du fichier.
    file_context = openFile(filename)

    #file_dehash : le texte déchiffré.
    file_dehash = cesarToText(file_context,key,alphalist)

    #créer un fichier déchiffré.
    filenamearr = filename.split('_')
    writeFile(filenamearr[0]+"_decode.txt",file_dehash)

"""test_code pour cesarTofile(filename,key,alphalist)

cesarTofile("test_code.txt",3,alphalist)

"""
