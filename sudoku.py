import itertools
import ortools.sat.python.cp_model
import numpy as np

class Sudoku:
    def build_model(self, new_grid):
        max_number = 9
        min_number = 1
        cell_size = 3
        size = cell_size**2
        self.size = size

        #### instance model
        self.model = ortools.sat.python.cp_model.CpModel()


        #### grid definition
        self.grid = {}
        for x in range(size):
            for y in range(size):
                self.grid[(x,y)] = self.model.NewIntVar(min_number, max_number, f"grid_val_{x}_{y}")
                if new_grid[y][x] != 0:
                    self.model.Add(self.grid[(x,y)] == new_grid[y][x])


        #### rows constraints
        for y in range(size):
            self.model.AddAllDifferent([self.grid[(x,y)] for x in range(size)])


        #### columns constraints
        for x in range(size):
            self.model.AddAllDifferent([self.grid[(x,y)] for y in range(size)])

        
        #### cells
        for y in range(cell_size):
            for x in range(cell_size):
                _x = np.array([3*x,3*x+1,3*x+2])
                _y = np.array([3*y,3*y+1,3*y+2])
                cell_elem = itertools.product(_x, _y)
                self.model.AddAllDifferent([self.grid[e] for e in cell_elem])
                #print([e for e in cell_elem])
                #print(50*"-")


    def solve(self):
        self.solver = ortools.sat.python.cp_model.CpSolver()
        status = self.solver.Solve(self.model)
        if status == ortools.sat.python.cp_model.OPTIMAL:
            for y in range(self.size):
                line = ""
                for x in range(self.size):
                    val = self.solver.Value(self.grid[(x,y)])
                    line += f"{val}"
                    if (x + 1) % 3 == 0:
                        line += "  "

                print(line)
                if (y + 1) % 3 == 0:
                    print("")


test_data = [
        [2,0,3, 0,4,0, 8,7,0],
        [8,0,0, 6,3,1, 0,0,2],
        [0,0,0, 8,0,0, 0,0,5],

        [0,0,0, 4,0,0, 5,0,9],
        [0,0,6, 9,8,7, 4,0,0],
        [3,0,9, 0,0,5, 0,0,0],

        [7,0,0, 0,0,6, 0,0,0],
        [4,0,0, 1,5,8, 0,0,7],
        [0,9,5, 0,2,0, 3,0,1],
        ]

sudoku = Sudoku()
sudoku.build_model(test_data)
sudoku.solve()
