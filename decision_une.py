import defiYahtzee

ENLETTRES = {1: 'As', 2: 'Deux', 3: 'Trois', 4: 'Quatre', 5: 'Cinq', 6: 'Six'} # Pour convertir les chiffres en lettres

#--------------------------------------------------------------------------------
#Fonction qui liste les possibilités de combinaisons à partir d'un lancer
#--------------------------------------------------------------------------------

def Possib(valeurDés):
    # Permet, à partir d'un lancer de dés, de déterminer les cases jouables à partir de ce lancer. Renvoie deux listes de couples. Ce sont des listes de couples, comportant la case jouable et les dés à garder dans une liste de 5 booléens nommé temp. La première liste, L_assur, contient les combinaisons que l'on a déjà à l'issus du lancer. La seconde liste, L_possib contient les possibilités atteignables à partir de ce lancer.
    
    L_assur=[]
    L_possib=[]
    ens_val={k for k in valeurDés}
    L_compt=[0,0,0,0,0,0]
    for k in valeurDés: # compte le nombre d'occurences de chaque valeur dans le lancer
        L_compt[k-1]+=1
    
    #SECTSUP
    for i in ens_val:
        temp=[True for j in range(5)] # liste de renvoie temporaire
        for j in range(5):
            if valeurDés[j]!=i:
                temp[j]=False
        L_assur.append((ENLETTRES[i],temp))
    
    #Full
    if 2 in L_compt:
        temp=[False for i in range(5)]
        if 3 in L_compt:
            L_assur.append(('Full',[True for i in range(5)]))
        else:
            L_compt_temp=L_compt.copy()
            i=L_compt_temp.index(2)
            L_compt_temp[i]=0
            if 2 in L_compt_temp:
                j=L_compt_temp.index(2)
                for k in range(5):
                    if valeurDés[k] in [i+1,j+1]:
                        temp[k]=True
                L_possib.append(('Full',temp))
    
    if 3 in L_compt:
        temp=[True for i in range(5)]
        if 2 in L_compt:
            L_assur.append(('Full',temp))
            
    #Petite suite
    trouve = False
    if len(ens_val)>=4:
        E1=[{1,2,3,4},{2,3,4,5},{3,4,5,6}]
        for e in E1:
            if e.issubset(ens_val):
                trouve = True
                temp=[False for i in range(5)]
                for j in range(5):
                    if valeurDés[j] in e:
                        temp[j]=True
                        e.remove(valeurDés[j])
                L_assur.append(('PetiteSuite',temp))
                break
    if not trouve:
        E2=[{2,3,4},{3,4,5}]
        for e in E2:
            if e.issubset(ens_val):
                temp=[False for i in range(5)]
                for j in range(5):
                    if valeurDés[j] in e:
                        temp[j]=True
                        e.remove(valeurDés[j])
                L_possib.append(('PetiteSuite',temp))
    
        

    #GrandeSuite
    if ens_val in [{1,2,3,4,5},{2,3,4,5,6}]:
        L_assur.append(('GrandeSuite',[True for i in range(5)]))
    
    else :
        if len(ens_val)>=4:
            E3=[{2,3,4,5},{1,2,3,4}]
            for e in E3:
                if e.issubset(ens_val):
                    temp=[False for i in range(5)]
                    for j in range(5):
                        if valeurDés[j] in e:
                            temp[j]=True
                            e.remove(valeurDés[j])
                    L_possib.append(('GrandeSuite',temp))
        
            
        
        
    
    #Brelan
    while 2 in L_compt:
        j=L_compt.index(2)
        temp=[True for i in range(5)]
        for k in range(5):
            if valeurDés[k]!=j+1 and valeurDés[k]:
                temp[k]=False
        L_possib.append(('Brelan',temp))
        L_compt[j]=0
    
    #Carré
    while 3 in L_compt:
        j=L_compt.index(3)
        temp=[True for i in range(5)]
        for k in range(5):
            if valeurDés[k]!=j+1 and valeurDés[k]:
                temp[k]=False
        L_assur.append(('Brelan',temp))
        L_possib.append(('Carre',temp))
        L_compt[j]=0
    
    #Yahtzee
    while 4 in L_compt:
        j=L_compt.index(4)
        temp=[True for i in range(5)]
        for k in range(5):
            if valeurDés[k]!=j+1:
                temp[k]=False
        L_assur.append(('Brelan',temp))
        L_assur.append(('Carre',temp))
        L_possib.append(('Yahtzee',temp))
        L_compt[j]=0
        
    while 5 in L_compt:
        j=L_compt.index(5)
        L_assur.append(('Yahtzee',[True for k in range(5)]))
        L_compt[j]=0
        
    #Chance
    L_assur.append(('Chance',[valeurDés[k] > 5 for k in range(5)]))
    
    return(L_assur[::-1],L_possib)












'''PREFERENCE = {'As': 13, 'Deux': 12, 'Trois': 10, 'Quatre': 9,
    'Cinq': 8, 'Six': 7, 'Brelan': 6, 'Carre': 5, 'Full': 4,
    'PetiteSuite': 3, 'GrandeSuite': 2, 'Yahtzee': 1, 'Chance': 11} # ordre de préférence dans lequelle on préférera tenter les combinaisons, liés à la difficultés de réalisations et aux nombres de points accordés'''

PREFERENCECHIFFRE = ['Yahtzee','GrandeSuite','Full','PetiteSuite','Carre','Brelan','Six','Cinq','Quatre','Trois','Deux','As','Chance']
# permet de determiner dans quelle case mettre un 0 en cas de impossibilité à jouer



def Nombre_Bon(L):# calcul le nombre de dés que l'on compte garder dans une liste
    compt = 0
    for el in L:
        if el:
            compt = compt + 1
    return compt



# calcul les points selon le choix fait (case) et un quintuplé de dés(valeurDes)
#index est une liste permettant de savoir pour la partie supérieure quelles sont les dés correspondant au choix


def calcul_point(feuillescore, valeurDes,case,index):
    if case == 'Yahtzee':
        return VALEURYAHTZEE
    if case == 'GrandeSuite':
        return VALEURGRANDESUITE
    if case == 'PetiteSuite':
        return VALEURPETITESUITE
    if case == 'Full':
        return VALEURFULL
    if case == 'Carre': 
        return sum(valeurDes) -5
    if case == 'Brelan':
        return sum(valeurDes) -10
    if case == 'Chance':
        return sum(valeurDes) -15 #­ permet de diminuer l'importance de la chance afin d'assurer un meilleur score sur cette case
    else :
        if calcul_ecart_bonus(feuillescore) <=9:
            if Nombre_Bon(index)>=3: # on remplit en priorité les hautes valeurs de sectSUP si on est "en avance" sur la prime et dans le cas contraire on choisira l'option qui fait "perdre" le moins de points par rapport au bonus
                return (ENCHIFFRES[case]*Nombre_Bon(index))
            else :
                return(3-(Nombre_Bon(index)*ENCHIFFRES[case]))
        else : 
            return (ENCHIFFRES[case]*Nombre_Bon(index))
             

def calcul_ecart_bonus(feuillescore):
    # permet de calculer le retard ou l'avance par rapport aux 63 points pour obtenir le bonus
    ecart = 0
    if feuillescore['As'] != None:
        ecart = ecart + feuillescore['As'] - 3
    if feuillescore['Deux'] != None:
        ecart = ecart + feuillescore['Deux'] - 6
    if feuillescore['Trois'] != None:
        ecart = ecart + feuillescore['Trois'] - 9
    if feuillescore['Quatre'] != None:
        ecart = ecart + feuillescore['Quatre'] - 12
    if feuillescore['Cinq'] != None:
        ecart = ecart + feuillescore['Cinq'] - 15
    if feuillescore['Six'] != None:
        ecart = ecart + feuillescore['Six'] - 18
    return ecart
    
    
def nombre_restant_bonus(feuillescore):
    #permet de savoir le nombre de case à remplir sur la section supérieur
    nombre  = 0 
    l = []
    if feuillescore['Six']  == None :
        nombre = nombre + 1
        l.append('Six')
    if feuillescore['Cinq']  == None :
        nombre = nombre + 1
        l.append('Cinq')
    if feuillescore['Quatre']  == None :
        nombre = nombre + 1
        l.append('Quatre')
    if feuillescore['Trois']  == None :
        nombre = nombre + 1
        l.append('Trois')
    if feuillescore['Deux']  == None :
        nombre = nombre + 1
        l.append('Deux')
    if feuillescore['As']  == None :
        nombre = nombre + 1
        l.append('As')
    return nombre,l
    
    
Feuillescore = {'As':  4, 'Deux': None, 'Trois': 6 , 'Quatre': 12,
    'Cinq': 20, 'Six': None, 'Brelan': None, 'Carre': None, 'Full': None,
    'PetiteSuite': None, 'GrandeSuite': None, 'Yahtzee': None, 'Chance': None,
    'PrimeYahtzee': 0}
    
    
calcul_ecart_bonus(Feuillescore)

def preference(feuillescore,feuillesoreAdv):
    # cette fonction donne l'ordre dans lequel on preferera remplir sa feuille de score
    dico = {}
    dico['Yahtzee'] = 0 # yahtzee toujours prioritaire
    dico['Chance'] = 12
    min = 1
    max = 11
    e = calcul_ecart_bonus(feuillescore)
    n,L = nombre_restant_bonus(feuillescore)
    if n <= 2: #on essaye d'assurer le bonus si on est pas loin de l'obtenir
        if abs(e) < 4:
            for elt in L:
                dico[elt] = min
                min = min +1
        else :
            for elt in L:
                dico[elt] = max
                max = max - 1
    # si le bonus est trop mal ou bien parti, on peut ne pas prioriser les cases qu'ils restent à remplir dans la SECTSUP
    else :
        for elt in L:
            dico[elt] = max
            max = max - 1
    if feuillescore['GrandeSuite'] == None and feuillescore['PetiteSuite'] == None: # on regarde si il reste des ensembles de cases qui nécessite des lancers similaires pour leur réalisation afin de cibler ces "familles" de cases
        dico['GrandeSuite'] = min
        dico['PetiteSuite'] = min + 1
        dico['Full'] = min + 2
        dico['Carre'] = min + 3
        dico['Brelan'] = min + 4
        min = min + 5
    else :
        if feuillescore['Full'] == None and Feuillescore['Carre'] == None :
            dico['Full'] = min
            dico['Carre'] = min + 1
            dico['GrandeSuite'] = min + 3
            dico['PetiteSuite'] = min + 4
            dico['Brelan'] = min + 2
            
        else:
            dico['GrandeSuite'] = min
            dico['PetiteSuite'] = min +1
            dico['Full'] = min + 2
            dico['Carre'] = min + 3
            dico['Brelan'] = min + 4
            min = min + 5
    return dico
    
    
            

def decision1(valeurDes, nrelancer, feuilleScore, feuilleScoreAdv):
    # fonction rendant la décision dans le cadre d'un comportement humain, en se basant sur une liste de préférence pour choisir les dés que l'on va relancer 
    a,b = Possib(valeurDes) 
    tout = a+b # liste contenant les possibilités jouables après le lancer
    prefer = preference(feuilleScore,feuilleScoreAdv)
    if nrelancer > 0: # on rend les dés que l'on souhaite conserver dans une liste de cinq booléens
        choix = []
        for el in tout : # on retire les cases déjà remplie au préalable dans la partie
            if feuilleScore[el[0]] == None:
                choix.append(el)
        if choix == [] : # si on a aucun choix possible on relance tous les dés
            return [False,False,False,False,False]
        else :
            pref = 13
            ind = 0
            for i in range (len(choix)) :
                if prefer[choix[i][0]] < pref: # on regarde, parmi les possibilités, laquelle nous préférons tenter selon un ordre de préférence global
                    pref = prefer[choix[i][0]]
                    ind = i
            return choix[ind][1]
    else :  # on rend la case que l'on veut jouer
        point = 0
        choix = a
        possib_finale = []
        for el in choix :
            if feuilleScore[el[0]] == None:
                possib_finale.append(el)
        if possib_finale == []:
            i = 0 # on doit donc décider de mettre 0 dans la case la plus difficile à obtenir 
            while feuilleScore[PREFERENCECHIFFRE[i]] != None:
                i = i+1
            return PREFERENCECHIFFRE[i]
        else : # on regarde, parmi les possibilités de choix, laquelle nous rapporte plus de points et on remplit la case associée
            ind = 0
            for i in range (len(possib_finale)) :
                if calcul_point(feuilleScore,valeurDes, possib_finale[i][0], possib_finale[i][1]) > point:     
                    point = calcul_point(feuilleScore,valeurDes, possib_finale[i][0], possib_finale[i][1])
                    ind = i
            return possib_finale[ind][0]
            
            
            
def decision2(valeurDes, nrelancer, feuilleScore, feuilleScoreAdv):
    # fonction rendant la décision dans le cadre d'un comportement humain, ici avec la volonté de réussir une combinaison à l'issue des cinq dés en relançant le moins de dés possible
    a,b = Possib(valeurDes) 
    tout = a+b # liste contenant les possibilités jouables après le lancer
    prefer = preference(feuilleScore,feuilleScoreAdv)
    if nrelancer >= 1: # on rend les dés que l'on souhaite conserver dans une liste de cinq booléens
        choix = []
        for el in tout : # on retire les cases déjà remplies au préalable dans la partie
            if feuilleScore[el[0]] == None:
                choix.append(el)
        if choix == [] : # si on a aucun choix possible on relance tous les dés
            return [False,False,False,False,False]
        else : 
            D = 5
            while D>=0: # on prends la case qui nous permet de relancer le plus petit nombre de dés
                for el in choix:
                    if Nombre_Bon(el[1]) == D and el[0] != 'Chance':
                        return el[1]
                D = D -1
    if nrelancer == 0:   # on rend la case que l'on veut jouer
        point = 0
        choix = a
        possib_finale = []
        for el in choix :
            if feuilleScore[el[0]] == None:
                possib_finale.append(el)
        if possib_finale == []:
            i = 0 # on doit donc décider de mettre 0 dans la case la plus difficile à obtenir 
            while feuilleScore[PREFERENCECHIFFRE[i]] != None:
                i = i+1
            return PREFERENCECHIFFRE[i]
        else : # on regarde, parmi les possibilités de choix, laquelle nous rapporte plus de points et on remplit la case associée
            ind = 0
            for i in range (len(possib_finale)) :
                if calcul_point(feuilleScore,valeurDes, possib_finale[i][0], possib_finale[i][1]) > point:     
                    point = calcul_point(feuilleScore, valeurDes, possib_finale[i][0], possib_finale[i][1])
                    ind = i
            return possib_finale[ind][0]
            
            
            
            


def poids1(case,valeurDes,index,feuilleScore):
    # poids attribué à la valeur de la case que l'on va viser, ici le poids sera d'autant plus important si la case a une valeur importante
    l = ['As','Deux','Trois','Quatre','Cinq','Six','Brelan','Carre','Full','PetiteSuite','GrandeSuite','Yahtzee','Chance']
    L = l[::-1]
    P = {'As': 0, 'Deux': 0, 'Trois': 0, 'Quatre': 0,
    'Cinq': 0, 'Six': 0, 'Brelan': 0, 'Carre': 0, 'Full': 0,
    'PetiteSuite': 0, 'GrandeSuite': 0, 'Yahtzee': 0, 'Chance': 0}
    for i in range (len(L)):
            if i>=7:
                if abs(calcul_ecart_bonus(feuilleScore))>=9:
                    P[L[i]] = Nombre_Bon(index)*defiYahtzee.ENCHIFFRES[L[i]]
                else :
                    P[L[i]] = (Nombre_Bon(index)*(defiYahtzee.ENCHIFFRES[L[i]] +35/3))# prise en compte de la PRIME
            else :
                if L[i] == 'Yahtzee':
                    P[L[i]] =  defiYahtzee.VALEURYAHTZEE
                if L[i] == 'GrandeSuite':
                    P[L[i]] =  defiYahtzee.VALEURGRANDESUITE
                if L[i] == 'PetiteSuite':
                    P[L[i]] = defiYahtzee.VALEURPETITESUITE
                if L[i] == 'Full':
                    P[L[i]] = defiYahtzee.VALEURFULL
                if L[i] == 'Carre': 
                    P[L[i]] = sum(valeurDes)# on estime que la valeur de la case sera proche de la somme des dés du lancer présent
                if L[i] =='Brelan':
                    P[L[i]] = sum(valeurDes) 
                if L[i] == 'Chance':
                    P[L[i]] = 0 # on veut jouer la chance en dernier recours
    return P
    


                    
def poids2(case,index,nrelancer):
    # poids attribué au chance de réussite, le poids augmente avec le taux de chance de réussite, le poids maximal est fixé à 50, soit la valeur de la case Yahtzee
    N = Nombre_Bon(index)
    if nrelancer == 2:
        if case == 'Full' or case == 'PetiteSuite' or case == 'GrandeSuite':
            return (50-(defiYahtzee.NDES-N)*2/3*10)/3 # on divise par 3 par rapport au cas où il reste un seul lancer, en effet beaucoup de lancer vont améliorer notre combinaison de départavnt d'arriver à 1 relancer, on peut donc prendre plus de risque
        else :
            if case in defiYahtzee.SECTSUP:# ici c'est le nombre de dés que l'on a déjà qui nous intéresse
                return N*7.5
            else :
                return (50-(defiYahtzee.NDES-N)*5/6*10)/3 #5/6 pour la proabilité d'echec à l'issus d'un lancer
    else :
        if case == 'Full' or case == 'PetiteSuite' or case == 'GrandeSuite':
            return 50-(defiYahtzee.NDES-N)*(2/3)*10
        else :
            if case in defiYahtzee.SECTSUP:
                return N*10
            else :
                return 50-(defiYahtzee.NDES-N)*(5/6)*10
            
            
def decision3(valeurDes, nrelancer, feuilleScore, feuilleScoreAdv):
    # fonction rendant la décision dans le cadre d'un comportement humain, ici avec la volonté de réussir une combinaison à l'issue des cinq dés en relançant le moins de dés possible
    a,b = Possib(valeurDes) 
    if nrelancer>0:
        l_choix = a+b # liste contenant les possibilités jouables après le lancer
        choix = [False,False,False,False,False]
        max  = 0
        liste_choix = []
        for el in l_choix: # on renvoie la décision qui maximise la somme poids1 + poids2, c'est à dire le maximum de points pour le minimum de risque.
            if feuilleScore[el[0]] == None or el[0] == 'Yahtzee':
                liste_choix.append(el)
        for el in liste_choix:
            if poids1(el[0],valeurDes,el[1],feuilleScore)[el[0]] + poids2(el[0],el[1],nrelancer)> max:
                choix = el[1]
                max = poids1(el[0],valeurDes,el[1],feuilleScore)[el[0]] + poids2(el[0],el[1],nrelancer)
        return choix
    if nrelancer == 0:   # on rend la case que l'on veut jouer
        point = 0
        choix = a
        possib_finale = []
        for el in choix :
            if feuilleScore[el[0]] == None:
                possib_finale.append(el)
        if possib_finale == []:
            i = 0 # on doit donc décider de mettre 0 dans la case la plus difficile à obtenir 
            while feuilleScore[PREFERENCECHIFFRE[i]] != None:
                i = i+1
            return PREFERENCECHIFFRE[i]
        else : # on regarde, parmis les possibilités de choix, laquelle nous rapporte plus de points et on remplie la case associé
            ind = 0
            for i in range (len(possib_finale)) :
                if calcul_point(feuilleScore,valeurDes, possib_finale[i][0], possib_finale[i][1]) > point:     
                    point = calcul_point(feuilleScore,valeurDes, possib_finale[i][0], possib_finale[i][1])
                    ind = i
            return possib_finale[ind][0]
            
            
        
        
        
    
        
    
                    
                    
            
                    
                    
                
                    
    
    
    

            
