# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:25:14 2016

@author: Groupe 8
"""

"Chemin pour les textes:"
textes='C:\\Users\Luke\L3 S2 Economie Maths\NLP\sample'
"Chemin pour la liste de mots"
commonwords='C:\\Users\Luke\L3 S2 Economie Maths\NLP\commonwords.txt'

import os
os.chdir(textes)
#ouvre le texte et le transforme en liste de mots           
def ouvrir(nomfichier):
   a=open(nomfichier,"r")
   b=a.read()
   b=b.lower()    
   alpha=['a','z','e','r','t','y','u','i','o','p','q','s','d','f','g','h','j','k','l','m','w','x','c','v','b','n',' ',"'",]
   b=b.split()
   print(b)
   vecmots=[]
   for i in range(len(b)):
       if '@' not in b[i]:
           vecmots.append(b[i])
   for i in range(len(vecmots)):
       for j in vecmots[i]:
           test=j in alpha
           if test==False:
               vecmots[i]=vecmots[i].replace(j,' ')
   truevecmots=[]
   for i in range(len(vecmots)):
       truevecmots.extend(vecmots[i].split())
   a=0
   while a<len(truevecmots):
       if truevecmots[a]=='':
           del(vecmots[a])
       a=a+1               
   return(truevecmots)
   
#transforme la liste en dico
def dico(nomfichier):
    f=ouvrir(nomfichier)
    res={}
    for i in f:
        res[i]=res.get(i,0)+1
    return(res)
    
#renvoie la fréquence de chaque mot sous forme de dictionnaire
def freq(nomfichier):
    tmp=ouvrir(nomfichier)
    ltmp=len(tmp)
    res=dico(nomfichier)
    for i in res:
        res[i]=100*res[i]/ltmp
    return(res)
    
# renvoie une liste des dictionnaires de fréquence pour chaque texte
listefichiers=os.listdir(textes) #listdir renvoie une liste des noms des documents contenus dans le fichier
res=[]
for i in listefichiers:
    res.append(freq(i))
res

# on calcule les fréquences totales

listdic=[] #il s'agit de la liste des dictionnaire dont on va se servir pour créer un dictionnaire avec le nombre d'apparitions du mot dans le corpus entier
for i in listefichiers:
    listdic.append(dico(i))


grodico={}
for i in range(len(listdic)):
    for j in listdic[i]:
        grodico[j]=grodico.get(j,0)+listdic[i][j]

n=0 #on calcule le nombre total de mots dans le corpus
for i in listefichiers:
    n=n+len(ouvrir(i))

freqtot={}
for i in grodico:
    freqtot[i]=grodico[i]/n

import time
from math import *


"""
Partie 2, question 1:
Calcul de tfidf : 
Etape 1 : On crée un dictionnaire répertoriant le nombre de texte où apparait un mot, pour tous les mots
Etape 2 : On définit la fonction tfidf qui pour un mot, calcule le tfidf de ce mot dans tout les textes
Etape 3 : On lance la fonction tfidf pour tous les mots présents dans le corpus
Note : le tout est chronométré
"""
start_time = time.time()  
#On va caculer pour tout les mots, dans combien de texte ils apparaissent
D={}
for i in listdic:
    for mot in i:
        D[mot]=D.get(mot,0)+1

def tfidf(mot):
    if not grodico.get(mot,0)==0:
       res=[]
       idf=log(float(len(listdic))/D[mot])
       for i in listdic:
           tf=i.get(mot,0)/(sum(i.values())) #on calcule d'abord tf
           res.append(tf*idf)
       return(res)
    return(0)



#On va faire une fonction qui prend un texte et calcule le TFIDF de chaque mot dedans
 
common=ouvrir(commonwords)
motcalcules=[]#l'astuce de stocker les mots pour ne pas les calculer deux fois évite 97867 appels de tfidf
listtfidf={}
calculevite=0
for i in listdic:
    for mot in i:
        if not mot in motcalcules and not mot in common:
            listtfidf[mot]=tfidf(mot)
            motcalcules.append(mot)
interval = time.time() - start_time  
print ('Temps pour calculer les tfidf de chaque mot dans chaque texte:', interval )
#Cette méthode calcule tout les indices en 182 secondes. C'est trop long, car on a qu'un sous ensemble de 996 textes...
"""
Partie 2, question 2:
Déterminer les n mots les plus pertinents : 
Etape 1 : On détermine dans chaque texte le mot le plus pertinent. Pour mieux se représenter la chose,
on peut imaginer une matrice avec en ligne les vecteurs donnés par la fonction tfidf et en colonne
l'indice de chaque texte. On boucle sur les colonnes (textes) et on recherche le maximum pour
chacunes d'elles
Etape 2 : On tri la liste (le tri se fait sur le premier indice de chaque élément)
Etape 3 : On découpe la liste pour ne garder que les n premiers termes
Note :  le tout est chronométré (résultat : 28 secondes)
        le temps d'éxécution ne dépend (presque) pas du nombre de mot pertinents souhaités
        le prof m'a conseillé de prendre deux ou trois mots par texte
"""
N=200 #nombre de mots pertinents
def motpertinent(n):
    maximot=[]
    for i in range(len(listtfidf[motcalcules[1]])):
        maximot1=(0,'')
        maximot2=(0,'')
        for j in listtfidf:
            if listtfidf[j][i]>maximot1[0]:
                maximot2 = maximot1
                maximot1=(listtfidf[j][i],j)
            elif listtfidf[j][i]>maximot2[0]:
                maximot2=(listtfidf[j][i],j)
        maximot.append(maximot1)
        maximot.append(maximot2)
    maximot.sort()
    maximot.reverse()
    long=len(maximot)
    for i in range(n,long):
        maximot.remove(maximot[n])
    return(maximot)
    
start_time = time.time()
pertinents=motpertinent(N)
interval = time.time() - start_time
print ('Temps pour calculer le mot max tfidf dans chaque texte:', interval )
    
"""
Partie 2, question 3:
Transformer les textes en vecteur de fréquences sur les n mots les plus pertinents : 
Etape 1 : pfreq sera une liste de liste, dont chacune représentera la fréquences des mots fréquents sur un texte
Etape 2 : pour chaque texte, on calcule sa liste
Note : le tout est chronométré (résultat :  croissant par rapport au nombre de mots pertinents choisi)
       il y a beaucoup de zéros
       en commentaire, j'ai ajouté la ligne pour faire la même chose avec le tfidf, ça me parait
       plus approprié, mais la question demande bien la fréquence.
"""
start_time = time.time()
pfreq=[]
for i in listdic:
    pfreqtexte=[]
    for mot in pertinents:
        pfreqtexte.append(i.get(mot[1],0)/(sum(i.values())))
        #pfreqtexte.append(tfidf(mot)[i]) 
    pfreq.append(pfreqtexte)
        
interval = time.time() - start_time
print ('Temps pour transformer les textes:', interval )
    
"""
Partie 2, question 4:
Calculer la distance cosinus entre deux textes : 
Etape 1 : ça ne sert à rien de calculer les distances entre les coordonnées nulles. Donc on va isoler les coordonnées non nulles 
Etape 2 : on calcul la distance cosinus. Si le dénominateur est nul, i.e. un des vecteurs ou les deux
        ont toutes leur coordonnées nulle, on renvoit 0 : aucune similarité
Note : pour calculer les distances cosinus de tout les textes entre eux, l'algo a tourner
       145 secondes (2min25) pour N=1000
       14.7 secondes pour N=100
       1.98 senconde pour N=10
"""

def dcos(vect1,vect2):
    numerator=0
    denominator=(0,0)
    for i in range(N):
        if not (vect1[i]==0 and vect2[i]==0):
            numerator=numerator+vect1[i]*vect2[i]
            denominator=(denominator[0]+vect1[i]**2,denominator[1]+vect2[i]**2)
    denominator=(sqrt(denominator[0]),sqrt(denominator[1]))
    if (denominator[0]==0 or denominator[1]==0):
        return(0)
    return(numerator/(denominator[0]*denominator[1]))

start_time = time.time()
cos=[]
for i in range(995):
    t=[]
    for j in range(995):
        t.append(dcos(pfreq[i+1],pfreq[1+j]))
    cos.append(t)
interval = time.time() - start_time
print ('Temps pour calculer la distance cos entre tous les couples de textes:', interval )

"""
Partie 3, question 1:
Déterminer automatiquement k groupes de textes homogènes à l’aide de l’algorithme kmeans :
Dans cette question nous utilisons l'algorithme kmeans pour créer k groupes de textes
Cet algorithme établit k moyennes (centres de groupe) et minimise la somme des distances aux moyennes pour tous les groupes
La distance utilisée ici est la distance cosinus déjà calculée, et stockée dans la liste pfreq

"""
import random

def kmeans(k):
    #Initialisation aléatoire
    centres=[]
    alea=random.sample(range(996),k)
    for i in range(k):
        centres.append(pfreq[alea[i]]) #Les centres sont des vecteurs de fréquences
    groupes=[-1]*996               #Le groupe de chaque texte

    done=False                    #Booléan pour l'arrêt de l'algorithme
    while not done:
        distances=[2]*996             #La distance de chaque texte à son centre
        done=True
        #Calcul de la distance de chaque texte au centre le plus proche
        for i in range(996):
            for j in range(k):
                if (k-1-j)!=groupes[i]:
                    temp=dcos(pfreq[i],centres[(k-j-1)])
                    print(temp)
                    #Si la distance est plus petite on change de groupe
                    if temp<distances[i]:
                        distances[i]=temp
                        groupes[i]=(k-j-1)
                        done=False
        #Calcul des nouveaux centres (moyennes des textes du groupe)
        moyenne=[[0]*N]*k    #k centres à n coordonnées
        compteur=[0]*k
        print(groupes)
        for i in range(996):
            l=groupes[i]
            moyenne[l]=moyenne[l]+pfreq[i]
            compteur[l]=compteur[l]+1
        for i in range(k):
            for j in range(N):
                moyenne[i][j]=moyenne[i][j]/compteur[i]
        centres=moyenne
    return(groupes)
            










