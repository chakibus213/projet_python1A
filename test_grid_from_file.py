# This will work if ran from the root folder (the folder in which there is the subfolder code/)
import sys 
sys.path.append("code/")

import unittest 
from grid import Grid
from solver import SolverGreedy, SolverEz

# fonction qui vérifie si une liste de paires est valide ( les paires sont valides et pas de cases prises deux fois)
def correct(grid, pairs):
    cases_prises=[]

    for ( (i1,j1), (i2, j2)) in pairs:
        if( not (grid.test_color( (i1, j1), (i2, j2)) or (i1,j1) in cases_prises or (i2, j2) in cases_prises ) ):
            return False 
            
        #on mémorise les cases
        cases_prises.append((i1,j1))
        cases_prises.append((i2,j2))
    return True

                    


#on teste les méthodes de la classe grid
class Test_GridLoading(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)

        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])
        self.assertEqual(grid.is_forbidden(1,1), False)
        self.assertEqual(grid.cost((0,0),(0,1)), 3)
        self.assertEqual(grid.all_pairs(), [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 1), (0, 2)), ((1, 1), (1, 2))])
        self.assertEqual(grid.counter_4(), 0)
        self.assertEqual(SolverGreedy(grid).score_g(), 14)
        

    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=False)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)

        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])
        self.assertEqual(grid.is_forbidden(0,1),False)
        self.assertEqual(grid.cost((0,0),(0,1)), 3)
        self.assertCountEqual(grid.all_pairs(), [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 1), (0, 2)), ((1, 1), (1, 2))])
        self.assertEqual(grid.counter_4(), 0)
        

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)

        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertCountEqual(grid.value, [[5, 8, 4], [11, 1, 3]])
        self.assertEqual(grid.is_forbidden(0, 1), True)
        self.assertEqual(grid.is_forbidden(1, 1), False)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 3)
        self.assertEqual(grid.cost(((0, 0), (1, 0))), 6)
        self.assertCountEqual(grid.all_pairs(), [((0, 0), (0, 1)),((0, 0), (1, 0)),((0, 1), (0, 2)),((1, 1), (1, 2))])
        self.assertEqual(grid.counter_4(), 1)
  

    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)

        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertCountEqual(grid.value, [[1, 1, 1], [1, 1, 1]])
        self.assertEqual(grid.is_forbidden(0, 1), True)
        self.assertEqual(grid.is_forbidden(1, 0), False)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 0)
        self.assertCountEqual(grid.all_pairs(), [((0, 0), (0, 1)),((0, 0), (1, 0)),((0, 1), (0, 2)),((1, 0), (1, 1))])
        self.assertEqual(grid.counter_4(), 1)
        


"""

#on teste les solver de la méthode gloutonne et de l'algorithme hongrois dans le cas général
class Test_CorrectResult(unittest.TestCase):

    #grilles 10 x20
    
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid11.in",read_values=True)

        #méthode gloutonne
        greedy = SolverGreedy(grid)

        score, pairs = greedy.run()

        self.assertTrue(correct(grid, pairs))
        print("La méthode gloutonne est correcte et le score est : ")
        print(score)

        #algorithme hongrois
        hungary = SolverEz(grid)

        score, pairs = hungary.run()

        self.assertTrue(correct(grid, pairs))
        print("L'algorithme hongrois est correcte et le score est : ")
        print(score)

    def test_grid2(self):

        grid = Grid.grid_from_file("input/grid14.in",read_values=True)

        #méthode gloutonne
        greedy = SolverGreedy(grid)

        score, pairs = greedy.run()

        self.assertTrue(correct(grid, pairs))
        print("La méthode gloutonne est correcte et le score est : ")
        print(score)

        #algorithme hongrois
        hungary = SolverEz(grid)

        score, pairs = hungary.run()

        self.assertTrue(correct(grid, pairs))
        print("L'algorithm hongrois est correct et le score est : ")
        print(score)
        
    def test_grid3(self):
        grid = Grid.grid_from_file("input/grid19.in",read_values=True)

        #méthode gloutonne
        greedy = SolverGreedy(grid)

        score, pairs = greedy.run()

        self.assertTrue(correct(grid, pairs))
        print("La méthode gloutonne est correcte et le score est : ")
        print(score)

        #algorithme hongrois
        hungary = SolverEz(grid)

        score, pairs = hungary.run()

        self.assertTrue(correct(grid, pairs))
        print("L'algorithme hongrois est correct et le score est : ")
        print(score)
     


    #grilles 100*200


    def test_grid4(self):
        grid = Grid.grid_from_file("input/grid21.in",read_values=True)

        #méthode gloutonne
        greedy = SolverGreedy(grid)

        score, pairs = greedy.run()

        self.assertTrue(correct(grid, pairs))
        print("La méthode gloutonne est correcte et le score est : ")
        print(score)

        
        #algorithme hongrois
        hungary = SolverEz(grid)

        score, pairs = hungary.run()

        self.assertTrue(correct(grid, pairs))
        print("L'algorithme hongrois est correcte et le score est : ")
        print(score)
        

    def test_grid5(self):

        grid = Grid.grid_from_file("input/grid24.in",read_values=True)

        #méthode gloutonne
        greedy = SolverGreedy(grid)

        score, pairs = greedy.run()

        self.assertTrue(correct(grid, pairs))
        print("La méthode gloutonne est correcte et le score est : ")
        print(score)

        
        #algorithme hongrois
        hungary = SolverEz(grid)

        score, pairs = hungary.run()

        self.assertTrue(correct(grid, pairs))
        print("L'algorithm hongrois est correct et le score est : ")
        print(score)
        
    
    def test_grid6(self):
        grid = Grid.grid_from_file("input/grid29.in",read_values=True)

        #méthode gloutonne
        greedy = SolverGreedy(grid)

        score, pairs = greedy.run()

        self.assertTrue(correct(grid, pairs))
        print("La méthode gloutonne est correcte et le score est : ")
        print(score)

        
        #algorithme hongrois
        hungary = SolverEz(grid)

        score, pairs = hungary.run()

        self.assertTrue(correct(grid, pairs))
        print("L'algorithme hongrois est correct et le score est : ")
        print(score)
        

        
"""
if __name__ == '__main__':
    unittest.main()
