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
                    i1, j1 = L0[i][0], L0[i][1]
                    i2, j2 = L1[1][0], L1[1][1]
                
                    L[i][j] = abs ( self.grid.value[i1][j1] - self.grid.value[i2][j2])  # Marque cette paire comme valide et met son poids dans la matrice d'adjacence
                    L[j][i] = abs ( self.grid.value[i1][j1] - self.grid.value[i2][j2])
                else:
                    L[i][j] = -1 # Marque cette paire comme non valide

        return L  

    def hungarian_algorithm(cost_matrix):
   
        cost_matrix = np.array(cost_matrix)
        row_ind, col_ind = linear_sum_assignment(-cost_matrix)  #linear_sum_assignment va donner le couplage de poids minimum donc on met un- pour que ca trouve le couplage de poids maximal
        return list(zip(row_ind, col_ind))

    def run(self):
        M=self.pairs2()
        return hungarian_algorithm(M)

                  
                    
        
                      

            

                



grille = Grid.grid_from_file(r"C:\Users\robin\OneDrive\Documents\Cours\prog25\input\grid04.in", read_values=False)



# Créer une instance de SolverGreedy en passant grille (instance de Grid)
sg = SolverEz(grille)



# Appeler la méthode score_g avec l'instance de Grid contenue dans sg
print("The final score of SolverGreedy is:", sg.score_g())



      

