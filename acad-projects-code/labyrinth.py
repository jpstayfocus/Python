#cette fonction retourne une liste contenant les nombres de 0 à n
def iota(n):
    return list(range(n))

#cette fonction indique si une liste tab contient un element egal à x    
def contient(tab, x):
    return x in tab

#cette fonction ajoute un élément à la fin d'une liste
def ajouter(tab, x):
    return tab if x in tab else tab.append(x)

#cette fonction retire un élément x d'une liste tab si elle est dedans
def retirer(tab, x):
    return tab.remove(x) if x in tab else tab

#cette fonction retourne une liste des cases voisines de l'entrée donnée           
def voisins(x,y,nX,nY):
    voisins = []
    N = x + y * nX
    O = x + y * (nX+1)
    #ajoute la case du haut si elle existe
    if N - nX >= 0:
        ajouter(voisins, (N-nX))
    #ajoute la case à gauche si elle existe
    if O % (nX+1) != 0:
        if y != 0 or x != 0:
            ajouter(voisins, (N-1))
    #ajoute la case en dessous si elle existe
    if N < nX * (nY-1):
        ajouter(voisins, (N+nX))
    #ajoute la case à droite si elle existe
    if (N+1) % nX != 0:
        ajouter(voisins, (N+1))
    return voisins

#cette fonction retourne un élément aléatoire d'une liste tab
def randObjTab(tab):
    return tab[math.floor(random()*len(tab))]

#cette fonction sert d'insersection de liste
def eleCommun(tab1, tab2):
    tab3 = []
    for element in tab1:
        if contient(tab2, element):
            ajouter(tab3, element)
    return tab3

#cette fonction dessine le labyrinthe de la fonction laby()
def dessiner(nX, nY, largeurCase, mursH, mursV):
    #definir les couleurs à utiliser
    black = struct(r=0,g=0,b=0)
    white = struct(r=15,g=15,b=15)
    
    #mettre l'écran en blanc
    setScreenMode(nX*(largeurCase+1)+1, nY*(largeurCase+1)+1)
    for i in range(nY*(largeurCase+1)+1):
            for j in range(nX*(largeurCase+1)+1):
                    setPixel(j, i, white)
    #initialiser au debut
    x = 0
    y = 0
    #dessiner les murs horizontaux
    for mur in range(nX*(nY+1)):
        if mur in mursH:
            for _ in range(largeurCase+1):
                setPixel(x,y, black)
                x += 1
            setPixel(x,y, black)
        else:
            for _ in range(largeurCase+1):
                x += 1
        #changer de ligne quand la condition est vraie
        if (mur+1)%nX == 0:
            x = 0
            y += largeurCase + 1
            
    #dessiner les murs verticaux        
    for mur in range((nX+1)*nY):
        #retourner à l'index x=0 quand on fini une rangée de murs
        if x > nX*(largeurCase+1):
            x = 0
        if mur in mursV:
            y = (mur//(nX+1)) * (largeurCase+1)
            for _ in range(largeurCase+1):
                setPixel(x,y,black)
                y += 1
            y = 0
        #permet de passer au mur suivant
        x += largeurCase + 1
    
    #l'entree du labyrinthe
    for x in range(largeurCase):
        setPixel(x+1, 0, white)
    #la sortie du labyrinthe
    for x in range(1,largeurCase+1):
        setPixel(nX*(largeurCase+1)-largeurCase+x-1,\
                 (nY+1)+nY*largeurCase-1,white)    
           
#cette fonction est l'algorithme qui crée le labyrinthe  

def laby(nX, nY, largeurCase):
    #assumer que tout les murs de la grille sont pleines
    mursH = iota(nX*(nY+1))
    mursV = iota((nX+1)*nY)

    #initialiser l'algorithme avec la premiere cave et les premiers front     
    cave =  [math.floor(random()*nX*nY)]
    xInit = cave[0]%nX
    yInit = int((cave[0]-(cave[0]%nX))/nX)
    front = voisins(xInit, yInit, nX, nY)
        
    #l'algorithme
    for i in range(nX*nY-1):
        #prendre un front au hasard
        #determiner ses coordonnées
        #et trouver les voisins, separant ceux qui sont dans la cave et ceux
        #qui ne le sont pas
        active = randObjTab(front)
        xCase = active%nX
        yCase = int((active-(active%nX))/nX)
        casesVoisines = voisins(xCase, yCase, nX, nY)

        casesAdj = eleCommun(cave, casesVoisines)
        
        #choisir une case adjacente au hasard
        activeAdj = randObjTab(casesAdj)
        
        #determiner quel mur qu'il faut effacer 
        if abs(active - activeAdj) == 1:
            if active > activeAdj:
                retirer(mursV, active+yCase)
            else:
                retirer(mursV, active+yCase+1)
        elif abs(active - activeAdj) == nX:
            if active > activeAdj:
                retirer(mursH, active)
            else:
                retirer(mursH, active+nX)
        
        #mise à jour de cave et front
        #front ne reçoit pas une valeur qu'elle a deja reçu
        ajouter(cave, active)
        for element in casesVoisines:
            ajouter(front, element)
        for element in eleCommun(cave, front):
            if contient(front, element):
                retirer(front, element)
    
    
    #dessiner le labyrinthe
    dessiner(nX, nY, largeurCase, mursH, mursV)
    #fin laby    
        
laby(16,9,20)
