# This will work if ran from the root folder (the folder in which there is the subfolder code/)
import sys 
sys.path.append("code/")

import unittest 
from grid import Grid
from solver import SolverGreedy, SolverEasy, SolverEmpty

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
        self.assertEqual(grid.all_pairs(), [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 1), (0, 2)), ((1, 1), (1, 2))])
        self.assertEqual(grid.counter_4(), 0)
        self.assertEqual(SolverEasy(grid).score_g(), 0)

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])
        self.assertEqual(grid.is_forbidden(0, 1), True)
        self.assertEqual(grid.is_forbidden(1, 1), False)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 3)
        self.assertEqual(grid.cost(((0, 0), (1, 0))), 6)
        self.assertEqual(grid.all_pairs(), [((0, 0), (0, 1)),((0, 0), (1, 0)),((0, 1), (0, 2)),((1, 1), (1, 2)),])
        self.assertEqual(grid.counter_4(), 1)
        self.assertEqual(Solver_Greasy(grille).score(), 1)
        self.assertEqual(SolverGreedy(grid).score_g(), 16)

    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])
        self.assertEqual(grid.is_forbidden(0, 1), True)
        self.assertEqual(grid.is_forbidden(1, 0), False)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 0)
        self.assertEqual(grid.all_pairs(), [((0, 0), (0, 1)),((0, 0), (1, 0)),((0, 1), (0, 2)),((1, 0), (1, 1)),])
        self.assertEqual(grid.counter_4(), 1)
        self.assertEqual(SolverGreedy(grid).score_g(), 2)
        self.assertEqual(SolverEasy(grid).score_g(), 0)

if __name__ == '__main__':
    unittest.main()
