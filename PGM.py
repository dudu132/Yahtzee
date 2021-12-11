
import numpy as np

#--------------------------------------------------------------------------------
#6**5=7776 combinaisons
#Sans l'ordre : 252, pkoi?
#--------------------------------------------------------------------------------

def toutes_les_combis():
    #cette fonction enumère dans une liste l'ensemble des 6^5 combinaisons de dés
    L=[]
    l=[0,0,0,0,0]
    for a in range(1,7):
        for b in range(1,7):
            for c in range(1,7):
                for d in range(1,7):
                    for e in range(1,7):
                        l[0]=a
                        l[1]=b
                        l[2]=c
                        l[3]=d
                        l[4]=e
                        L.append(l.copy())
    return(L)
                        
 

def valeurs(l):
    v=set()
    for k in l:
        v.add(k)
    return(v)

def compare_valeurs(l1,l2):
    t2=l2.copy()
    for i in l1:
        for j in t2:
            if i==j:
                t2.remove(j)
                break
    if t2==[]:
        return(True)
    else:
        return(False)
    
    
def tri_combi(L):
    #on élimine de l'ensemble des combinaisons les combinaisons que l'on retrouve plusieurs fois, pour obtenir 252 combinaisons ordonnées
    L2=[]
    n=len(L)
    for i in range(n):
        c=0
        for j in range(i,n):
            if i!=j and compare_valeurs(L[i],L[j])==False:
                c+=1
        if c==n-i-1:
            L2.append(L[i])
            
    return(L2)

TCOMBI = toutes_les_combis()
LISTECOMBI = tri_combi(TCOMBI.copy())

#print(len(tri_combi()))



#--------------------------------------------------------------------------------
#Calcul des espérances
#--------------------------------------------------------------------------------
#Renvoie la liste de tous les sous-ensembles de taille n d'une liste
def n_uplet(valeurDes,n):
    N=5
    L=[]
    if n==1:
        L=[[k] for k in range(N)]
    else:
        L2=n_uplet(valeurDes,n-1)
        for k in range(N):
            for l in L2:
                if k not in l:
                    L.append([k]+l)
    return(tri_combi(L))
    
#Verifie que L1 est dans L2
def list_in_list(L1,L2):
    e1=L1.copy()
    e2=L2.copy()
    for k in e1:
        if k in e2:
            e1.remove(k)
            e2.remove(k)
    if e1==[]:
        return(True)
    return(False)
    
    

#--------------------------------------------------------------------------------
#Création du tableau
#--------------------------------------------------------------------------------



def tableau_vierge():
    T=np.zeros((252,13))
    L=toutes_les_combis()
    for k in range(252):
        T[k,0]=str(L[k])
    return(T)




import defiYahtzee



def combipossible(choixrelancer,valeurDes):
    #La fonction permet, en prenant une combinaison de dés et un choix des dés à relancer sous forme d'une 5-liste de 0 ou 1,d'obtenir l'ensemble des combinaisons possibles au lancer suivant
    deja = False
    support = [0,0,0,0,0]
    nombre_garde = 5
    combipossible = []
    for i in range(5):
        if choixrelancer[i] == 1:
            support[i] = valeurDes[i]
            nombre_garde -= 1
    if nombre_garde == 0:
        return([valeurDes])
    for i1 in range(6):
        deja = False
        j1 = 0
        while choixrelancer[j1] != 0:
            j1 = j1+1
        if nombre_garde > 1:
            for i2 in range(6):
                deja = False
                j2 = j1 + 1
                while choixrelancer[j2] != 0:
                    j2 = j2+1
                if nombre_garde > 2:
                    for i3 in range(6):
                        deja = False
                        j3 = j2 + 1
                        while choixrelancer[j3] != 0:
                            j3 = j3+1
                        if nombre_garde > 3:
                            for i4 in range(6):
                                deja = False
                                j4 = j3 + 1
                                while choixrelancer[j4] != 0:
                                    j4 = j4+1
                                if nombre_garde > 4:
                                    for i5 in range(6):
                                        deja = False
                                        j5 = j4 + 1
                                        l = support.copy()
                                        l[j1] = i1 + 1
                                        l[j2] = i2 + 1
                                        l[j3] = i3 + 1
                                        l[j4] = i4 + 1
                                        l[j5] = i5 + 1
                                        combipossible.append(l)
                                        deja = True
                                else :
                                    if not deja:
                                        l = support.copy()
                                        l[j1] = i1 + 1
                                        l[j2] = i2 + 1
                                        l[j3] = i3 + 1
                                        l[j4] = i4 + 1
                                        combipossible.append(l)
                                        deja = True
                        else :
                            if not deja:
                                l = support.copy()
                                l[j1] = i1 + 1
                                l[j2] = i2 + 1
                                l[j3] = i3 + 1
                                combipossible.append(l)
                                deja = True
                else :
                    if not deja:
                        l = support.copy()
                        l[j1] = i1 + 1
                        l[j2] = i2 + 1
                        combipossible.append(l)
                        deja = True
        else :
            if not deja :
                l = support.copy()
                l[j1] = i1 + 1
                combipossible.append(l)

    return combipossible






def touslesrelancers():
    #Renvoie l'ensemble des choix possible de dés à relancer, soit une liste de 32 CHOIX
    T = []
    for i1 in range(2):
        for i2 in range(2):
            for i3 in range(2):
                for i4 in range(2):
                    for i5 in range(2):
                        T.append([i1,i2,i3,i4,i5])
    return T

RELANCERS = touslesrelancers()

## premier relancer

def esperance_rel1(valeurDes,case):
    T = np.zeros((32))
    for i in range(32):
        E = 0
        liste_combi = combipossible(RELANCERS[i],valeurDes)
        for j in range(len(liste_combi)):
            if defiYahtzee.respecteRegles(case,defiYahtzee.FEUILLESCOREVIERGE,False,valeurDes):
                E = E + defiYahtzee.calculScore(liste_combi[j],case,)
        T[i] = (E/len(liste_combi))
    return T
    
ESPERANCE = np.zeros((252,13,2,32))

ORDRE_CASE = {'As': 0, 'Deux': 1, 'Trois': 2, 'Quatre': 3,'Cinq': 4, 'Six': 5, 'Brelan': 6, 'Carre': 7, 'Full': 8,'PetiteSuite': 9, 'GrandeSuite': 10, 'Yahtzee': 11, 'Chance': 12}

def transformation(L):
    #transforme les combinaisons de dés en chaine de caractères
    c =''
    for i in range(len(L)):
        c = c + str(L[i])
    return c
    
INDICE = {}
for i in range(len(LISTECOMBI)):
    INDICE[transformation(LISTECOMBI[i])] = i
#Ici on stock dans un dictionnaire un entier correspondant à chaque combinaison triée de dés, afin de pouvoir retrouver facilement dans le tableau des espérances les valeurs que l'on cherche
        
        

def Esperance_rel1(valeurDes,case):
    # compléte le tableau des espérances quand il ne reste qu'un lancer avant de rendre la décision finale
    for i in range(32):
        E = 0
        liste_combi = combipossible(RELANCERS[i],valeurDes)
        for j in range(len(liste_combi)):
            if defiYahtzee.respecteRegles(case,defiYahtzee.FEUILLESCOREVIERGE,False,valeurDes):
                E = E + defiYahtzee.calculScore(liste_combi[j],case,)
        #on somme les points que l'on obtient pour toutes les combinaisons possible selon les dés gardés
        ESPERANCE[INDICE[transformation(valeurDes)],ORDRE_CASE[case],0,i] = E/len(liste_combi)
   

import time

start = time.time()
        
Esperance_rel1([6,6,5,4,4],'Brelan')
E1 = ESPERANCE[INDICE[transformation([6,6,5,4,4])],ORDRE_CASE['Brelan']]

end = time.time()

print(end - start)

start = time.time()

L = ['Yahtzee','GrandeSuite','Full','PetiteSuite','Carre','Brelan','Six','Cinq','Quatre','Trois','Deux','As','Chance']
for el in LISTECOMBI:
    for el2 in L:
        Esperance_rel1(el,el2)

#134 s sur mon ordi perso
# 161 s ordi portable
end = time.time()

print(end - start)
## passage au deuxième relancers

def ordonner(L):
    #tri bulle d'une liste
    T = L.copy()
    for i in range(5):
        for j in range(i,5):
            if T[i]<T[j]:
                a = T[i]
                T[i] = T[j]
                T[j] = a
    return T

def esperance_rel2(valeurDes,case):
    T = np.zeros(32)
    for i in range(32):
        E = 0
        liste_combi = combipossible(RELANCERS[i],valeurDes)
        for j in range(len(liste_combi)):
            E = E + sum(ESPERANCE[INDICE[transformation(ordonner(liste_combi[j]))],ORDRE_CASE[case],0,:])/32
        T[i] = E/len(liste_combi)
    return T
            
E2 = esperance_rel2([2,5,2,3,3],'Brelan')
print(E2)
    
def Esperance_rel2(valeurDes,case):
       # compléte le tableau des espérances quand il ne reste que 2 lancer avant de rendre la décision finale
    for i in range(32):
        E = 0
        liste_combi = combipossible(RELANCERS[i],valeurDes)
        for j in range(len(liste_combi)):
            E = E + sum(ESPERANCE[TINDICE[transformation(liste_combi[j])],ORDRE_CASE[case],0,:])/32
        # ici on utilise les espérances déjà calculés précedemment pour obtenir ces nouvelles espérances, en faisant une moyennes des espérances pour 1 lancer restant
        ESPERANCE[TINDICE[transformation(valeurDes)],ORDRE_CASE[case],1,i] = E/len(liste_combi)
    
         
start = time.time()
        
Esperance_rel2([6,6,5,4,4],'Brelan')
E3 = ESPERANCE[INDICE[transformation([6,6,5,4,4])],ORDRE_CASE['Brelan']]

end = time.time()

print(end - start)

start = time.time()

for el in LISTECOMBI:
    for el2 in L:
        Esperance_rel2(el,el2)


# 611 s ordi portable(un peu long probablement)
# 427 s en utilisant TINDICE directement
end = time.time()
print(end - start)

TINDICE = {}
for i in range(len(TCOMBI)):
    TINDICE[transformation(TCOMBI[i])] = INDICE[transformation(ordonner(TCOMBI[i]))]
# même idée que pour INDICE, mais cette fois ci pour les 6^5 combinaisons, auxquelles on attribue l'entier de la combinaison ordonnée

