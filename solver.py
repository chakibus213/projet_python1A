from grid import Grid
class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()

    def score(self):
        """
        Computes the score of the list of pairs in self.pairs
        """
        res= 0
        cases_prises=[]

        #calcul le score généré par les paires choisis
        for element in self.pairs:

            i1, j1 = element[0][0], element[0][1]
            i2, j2 = element[1][0], element[1][1]

            cases_prises.append( (i1, j1) )
            cases_prises.append( (i2, j2) )

            res += abs ( self.grid.value[i1][j1] - self.grid.value[i2][j2])

        #calcul le score généré par les cases restantes
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if not (i,j) in cases_prises and self.grid.color[i][j] != 4:
                    res += self.grid.value[i][j]


        return res

class SolverEmpty(Solver):
    def run(self):
        pass




class SolverGreedy(Solver):
    def __init__(self, grid):
        super().__init__(grid)

    def tri_pairs(self, liste_paires):  #tri une liste de paires en fonction de leur coût
        temp = [] #on crée une liste contenant les coûts de chacune des paires 
        compteur = 0
        for element in liste_paires:  #on la trie par ordre décroissant selon leur coût
            
            i1, j1 = element[0][0], element[0][1]
            i2, j2 = element[1][0], element[1][1]

            

            temp.append( -(abs ( self.grid.value[i1][j1] - self.grid.value[i2][j2]), compteur)) 

            compteur += 1
        
        temp.sort(key=lambda x: x[0])

        res = []

        # on met dans res les paires de liste_paires triès selon leur coût
        for k in range(len(liste_paires)):
            res.append(liste_paires[temp[k][1]])

        return res

    def greedy_method(self):
        """
        Calcule un score en utilisant une approche gloutonne.
        L'objectif est de sélectionner des paires valides jusqu'à ce qu'il y en ai plus de disponibles, sans réutiliser les mêmes cases.
        """
        s = 0  # Score initialisé à 0
        L1 = []  # Liste des cases déjà appariées
        L = self.tri_pairs ( self.grid.all_pairs())  # Liste des paires valides disponibles trièes 

        # On parcourt chaque paire et on l'ajoute si elle n'entre pas en conflit avec une paire existante
        for i in L:
            if i[0] not in L1 and i[1] not in L1:  # Vérifie que les deux cases ne sont pas déjà utilisées
                s += self.grid.cost(i)  # Ajoute le coût de cette paire au score total
                L1.append(i[0])  # Marque la première case comme utilisée
                L1.append(i[1])  # Marque la seconde case comme utilisée

        # Ajoute ensuite la valeur des cases qui n'ont pas été utilisées dans une paire
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i, j) not in L1:
                    s += self.grid.value[i][j]

        return (s,L)  # Retourne la liste des paires et le score final
    
    def run(self):
        return self.greedy_method()[1]


class SolverEz(Solver):
    def __init__(self, grid):
        """
        Initialise le solveur en séparant la grille en deux groupes :
        - L0 : cases dont la somme des indices est paire
        - L1 : cases dont la somme des indices est impaire
        On crée ensuite une matrice pour représenter les connexions possibles entre ces deux groupes.
        """
        super().__init__(grid)
        self.Lc = []  # Liste des paires sélectionnées
        self.L, self.L0, self.L1 = self.pairs2()  # Génération des groupes des cases paires et impaires et de la matrice de connexions
        self.La = [row[:] for row in self.L]# Copie de la matrice des connexions pour modifications

    def pairs2(self):
        """
        Divise la grille en deux groupes de cases (L0 et L1) et crée une matrice L
        indiquant quelles paires sont possibles entre ces groupes.
        """
        L0 = []  # Liste des cases paires
        L1 = []  # Liste des cases impaires

        # Remplissage des listes L0 et L1 en fonction de la parité des indices
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i + j) % 2 == 0:
                    L0.append((i, j))
                else:
                    L1.append((i, j))

        # Création de la matrice d'adjacence L pour représenter les connexions possibles entre L0 et L1
        L = [[0 for k in range(len(L1))] for k1 in range(len(L0))]
        for i in range(len(L0)):
            for j in range(len(L1)):
                if (L0[i], L1[j]) in self.grid.all_pairs() or (L1[j], L0[i]) in self.grid.all_pairs():
                    L[i][j] = 1  # Marque cette paire comme valide
                    L[j][i] = 1
                else:
                    L[i][j] = 0 # Marque cette paire comme non valide

        return L, L0, L1  # Retourne la matrice d'adjacence et les listes des groupes








    def score_g(self):
        """
        Calcule un score en essayant de former le maximum de paires tout en respectant les contraintes de la grille.
        """

        for i in range(len(self.La)):
            self.success = False # Re initialise le succès à False à chaque itération
            # Ignore les cases interdites
            if self.grid.is_forbidden(self.L0[i][0], self.L0[i][1]):
                continue

            # Si une paire est immédiatement disponible, on l'ajoute
            if 1 in self.La[i]:  
                ind = self.La[i].index(1)  # Trouve la première paire possible
                self.Lc.append((self.L0[i], self.L1[ind]))  # Ajoute la paire à la solution

                # Supprime la connexion potentielle entre la case impaire ind et les autres cases paires
                for k in range(len(self.La)):
                    self.La[k][ind] = 0
            else:
                # Si aucune paire directe n'est trouvée, on tente d'en former une via la récursion
                if self.recur(i, self.La, self.Lc, [])[3]: # Si il existe un chemin tel que la case i trouve une paire et toutes celles qui en avait déja avant aussi
                    self.La, self.Lc, success = self.recur(i, self.La, self.Lc, [])
            
                
        return (self.grid.n * self.grid.m - 2 * len(self.Lc),self.Lc) # Calcul du score final en soustrayant au nombre total de cases, les nombres sans paire et les cases noires

    def recur(self, i, La1, Lc, visited):
        """
        Fonction récursive permettant de trouver une paire quand l'approche principale ne trouve rien immédiatement.
        """
        Lc1 = Lc[:]# On copie la liste Lc pour pouvoir faire des modifications temporaires sans modifier Lc

        # Si une paire est disponible directement, on la sélectionne
        if 1 in La1[i]:
            ind = La1[i].index(1)
            self.Lc.append((self.L0[i], self.L1[ind]))  # Ajoute cette paire à la solution


            # Supprime la connexion potentielle entre la case impaire ind et les autres cases paires
            for k in range(len(La1)):
                La1[k][ind] = 0

            return La1, Lc1,True  # Retourne les mises à jour (avec succès = True)

        else:
            # Exploration en profondeur pour essayer de former une paire indirectement
            for j in range(len(self.L[i])): #on parcourt toutes les connexions potentielles initiales de la case paire i
                if self.L[i][j] == 1 and j not in visited: #seulement si on n'a pas déja visité cette case pendant la recursion
                    new_visited = visited[:]  # Copie de la liste visited pour que visited reste inchangé entre deux iterations de j
                    new_visited.append(j)  # Ajoute l'index de la case impaire visitée pour éviter les boucles infinie

                    

                    # Retrouve la case paire avec laquelle elle etait initalement connectée, et chercher une nouvelle paire à cette case paire recursivement
                    for c in Lc1: 
                       if c[1] == self.L1[j]: # On ignore si elle était en premiere ou seconde place de la paire
                            Lc1.remove((c[0], c[1]))  # On supprime l'ancienne paire de la liste solution temporaire
                            Lc1.append((self.L0[i], self.L1[j]))  # Ajoute la paire dans la liste solution temporaire
                            self.recur(self.L0.index(c[0]), La1, Lc1, new_visited)
                            if self.recur(self.L0.index(c[0]), La1, Lc1, new_visited)[3]:
                                return self.recur(self.L0.index(c[0]), La1, Lc1, new_visited)
                       elif if c[0] == self.L1[j]:
                            Lc1.remove((c[0], c[1])) #On supprime l'ancienne paire de la liste solution temporaire
                            Lc1.append((self.L0[i], self.L1[j])) # Ajoute la paire dans la liste solution temporaire
                            if self.recur(self.L0.index(c[1]), La1, Lc1, new_visited)[3]: # Si il existe un chemin tel que la case i trouve une paire et toutes celles qui en avait déja avant aussi
                                return self.recur(self.L0.index(c[1]), La1, Lc1, new_visited)    
            return self.La, self.Lc,False  # Aucune modification n'est faite si on n'a pas reussi à trouver une paire à chacune des cases qui étaient déja prises

                  
                    
        
                      

            

                



grille = Grid.grid_from_file(r"C:\Users\robin\OneDrive\Documents\Cours\prog25\input\grid04.in", read_values=False)



# Créer une instance de SolverGreedy en passant grille (instance de Grid)
sg = SolverEz(grille)



# Appeler la méthode score_g avec l'instance de Grid contenue dans sg
print("The final score of SolverGreedy is:", sg.score_g())



      

