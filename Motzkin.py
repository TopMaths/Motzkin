# Proposé par Top Maths sans aucune garantie


"""
Description du module Motzkin pour illustrer
 la vidéo de Top Maths sur Youtube : les nombres de Motzkin

Les fonctions principales sont 
- NbMotzkin(n)
  qui renvoie le nombre de Motzkin d'ordre l'entier n 

- CodesMotzkin(n)
  qui renvoie la liste de tous les codes de Motzkin de longueur l'entier n

- trace(s)
  qui trace pour un code de Motzkin s, sur une même figure
  --> le cercle avec les cordes disjointes
  --> le mot de Motzkin
  --> le chemin de Motzkin
  --> l'arbre unaire-binaire
comme ils ont été définis dans la vidéo

les autres fonctions servent juste à construire celles-là.
"""

class MotzkinError(Exception):
    """pour vérifier que l'on utilise bien un code de Motzkin"""
    def __init__(self, liste):
        self.liste=liste
        Exception.__init__(self, "{} sequence de Motzkin invalide".format(liste))


def NbMotzkin(n):
    """Renvoie le nombre de Motzkin M(n) en utilisant 
la relation de récurrence :
$M_{n+2} = \frac{2n+5}{n+4} M_{n+1} 
           + \frac{3n+3}{n+4}M_{n}$ """ 

    M0=M1=1
    for k in range(0,n):
        M0,M1=M1,((2*k+5)*M1+(3*k+3)*M0)//(k+4)
    return M0

def CodesMotzkin(n):
    """renvoie la liste de tous les codes de Motzkin de longueur l'entier n"""
    if n==0:
        return [[]]
    else:
        L=CodesMotzkin(n-1)
        for x in L: x.append(0)
        for k in range(2,n+1):
            A=CodesMotzkin(k-2)
            B=CodesMotzkin(n-k)
            for a in A:
                for b in B:
                    ell=[]
                    ell.extend(a)
                    ell.append(1)
                    ell.extend(b)
                    ell.append(-1)
                    L.append(ell)
    return L

import matplotlib.pyplot as plt
import numpy as np

def cercle(n=361):
    """renvoie les listes d'abscisses et d'ordonnées de points sur le cercle unité""" 
    t=np.linspace(0,2*np.pi,n)
    x=np.cos(t)
    y=np.sin(t)
    return x,y


def isMotzkin(s):
    """vérifie que s est bien un code de Motzkin"""
    if type(s)!= type([]) and type(s)!= type(()): return False
    Som=0
    for i in s:
        # s ne peut contenir que les entiers -1,0,1
        if type (i)!=type(1) or abs(i)>1: return False
        Som+=i
        # si Som<0 : le chemin correspondant passe sous l'axe des abscisses
        if Som<0: return False
    #si Som>0 le point d'arrivée du chemin n'est pas sur l'axe des abscisses 
    return Som==0


def associe(s,k):
    """recherche l'arete associée au k ième caractère du code de Motzkin s"""
    if not isMotzkin(s): raise MotzkinError(s)
    S,j=s[k],k
    while S!=0:
        j+=s[k]
        S+=s[j]
    return j

def point(k,n):
    """retourne le point du cercle unité d'agument 2.k.pi/n""" 
    return np.cos(2*k*np.pi/n), np.sin(2*k*np.pi/n)

def arete(s):
    """renvoie la liste des aretes associées au code de motzkin s """
    if not isMotzkin(s): raise MotzkinError(s)
    L=[]
    for i,j in enumerate(s):
        if j>0: L.append((i,associe(s,i)))
    return L

def dot(pos,colsom, markersize):
    """marque à point à la position indiquée"""
    plt.plot(*pos,marker=".",color=colsom, markersize=markersize)

def drawarete(pos1,pos2,colar):
    plt.plot([pos1[0],pos2[0]], [pos1[1],pos2[1]],color=colar)

def placeetiq(pos, no,distetiq=.1):
    plt.text(pos[0]-distetiq, pos[1],"${}$".format(no), horizontalalignment='center',verticalalignment='center' )


def drawarbre(s,etiq,pos, dx,dy, colar, colsom,markersize):
    """trace l'arbre associé au code de Motzkin"""
    if not isMotzkin(s): raise MotzkinError(s)
    if (s==[]):
        dot(pos,colsom,markersize);
        return
    if (s[0]==0):
        pos2=(pos[0], pos[1]-dy)
        drawarete(pos,pos2 ,colar)
        dot(pos,colsom,markersize)
        dot(pos2,colsom,markersize)
        placeetiq(pos2,etiq[0])
        drawarbre(s[1:],etiq[1:], pos2, dx/2, dy, colar, colsom,markersize)
        return
    
    else:
        k=associe(s,0)
        pos2a,pos2b=(pos[0]-dx, pos[1]-dy), (pos[0]+dx, pos[1]-dy)   
        drawarete (pos,pos2a,colar)
        drawarete(pos,pos2b,colar)
        dot(pos,colsom,markersize)
        dot(pos2b,colsom,markersize)
        placeetiq(pos2b,etiq[0])
        dot(pos2a,colsom,markersize)
        placeetiq(pos2a,etiq[k])
        drawarbre(s[1:k],etiq[1:k], pos2b, dx/2,dy, colar, colsom,markersize)
        drawarbre(s[k+1:], etiq[k+1:], pos2a, dx/2,dy, colar, colsom,markersize)
        return

def trace(s, save=False, larg=16,haut=9):
    """
 Trace pour un code de Motzkin s, sur une même figure
  --> le cercle avec les cordes disjointes
  --> le mot de Motzkin
  --> le chemin de Motzkin
  --> l'arbre unaire-binaire
comme ils ont été définis dans la vidéo

l'option save à True enregsitre le fichier sous le nom Code, suivi d'un numéro
obtenu en ajoutant 1 à chaque valeur du code, avec l'extension pdf

avec l'instruction : 
>>> trace([1,0,-1], save=True)

   le fichier de sauvegarde sera Code210.pdf

les paramètres larg et haut permettent d'ajuster les dimension de l'image sauvegardée
"""
    if not isMotzkin(s): raise MotzkinError(s)
    plt.figure(figsize=(larg,haut))
    plt.suptitle("Code de Motzkin {}".format(s), fontsize=24)
    # tracer un cercle avec des cordes disjointes
    plt.subplot(2,2,1)
    plt.axis('off')
    col=(1,.5,.2)
    plt.plot(*cercle())
    n=len(s)
    L=arete(s)
    for a,b in L:
        xa,ya=point(a,n)
        xb,yb=point(b,n)
        plt.plot([xa,xb],[ya,yb],color=col)
    for i in range(n):
        xa,ya=point(i,n)
        c=1.1
        plt.plot(xa,ya,'bo')
        plt.text(c*xa,c*ya,"${}$".format(i), horizontalalignment='center',verticalalignment='center', )

    # écrire le mot de Motzkin
    plt.subplot(2,2,2)
    plt.axis('off')    
    sizemot=20
    STR=[")", "-", "("]
    for i in range(n):
        plt.text((i+1)/(n+1),0.5,STR[s[i]+1], fontsize=sizemot)

    # tracer le chemin de Motzkin
    plt.subplot(2,2,3)
    plt.axis('off')
    colpath,colsom=(.5,1,.5),(1,0,0)
    sizesom=10
    xi=yi=0
    for i in range(n):
        xf,yf=xi+1,yi+s[i]
        plt.plot([xi,xf],[yi,yf], color=colpath)
        plt.plot(xi,yi,color=colsom,marker='.',markersize=sizesom)
        xi,yi=xf,yf
    plt.plot(xi,yi,color=colsom,marker='.',markersize=sizesom)

    # tracer l'arbre unaire-binaire
    plt.subplot(2,2,4)
    plt.axis('off')

    posracine=(0,0)
    colar=(1,1,0)
    colsom=(0,1,1)
    markersize=10
    etiq=list(range(n))
    drawarbre(s, etiq, posracine, 1,1,colar,colsom,markersize)

    if save:
        fichier="Code"+"".join([str(x+1) for x in s])+".pdf"
        print("Enregistré dans "+ fichier)
        plt.savefig(fichier)
    else:
        plt.show()
    

