import os
import random
from collections import deque

class Environment:
    def __init__(self, maze=__file__):
        self.maze = self.load_maze(maze_file)
        self.original_maze = [row [:] for row in self.maze] if self.maze else None
        sel.agent_pos = self.find_agent_start()
        self.food_count = self.count_food()
        self.steps = 0
    
    def load_maze(self, maze_file):
        maze = []
        try:
            with open(maze_file, 'r') as file:
                for line in file:
                    maze.append(list(line.strip()))
                return maze
        except FileNotFoundError:
            print (f"Arquivo {maze_file} não encontrado!")
            return None
    
    def find_agent_start(self):
        if not self.maze:
            return None
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == 'E':
                    return (i,j)
            return None
    
    def count_food(self):
        if not self.maze:
            return 0
        count = 0
        for row in self.maze:
            count += row.count ('o')
            return count
        
    def get_sensor(self, pos, direction):
        sensor_matrix = [['X' for _ in range (3)] for _ in range (3)]

        dir_offsets = {
            'N': [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),  (0, 0),  (0, 1),
                  (1, -1),  (1, 0),  (1, 1)],
            'S': [(1, 1),   (1, 0),   (1, -1),
                  (0, 1),   (0, 0),   (0, -1),
                  (-1, 1),  (-1, 0),  (-1, -1)],
            'L': [(-1, 1),  (0, 1),   (1, 1),
                  (-1, 0),  (0, 0),   (1, 0),
                  (-1, -1), (0, -1),  (1, -1)],
            'O': [(1, -1),  (0, -1),  (-1, -1),
                  (1, 0),   (0, 0),   (-1, 0),
                  (1, 1),   (0, 1),   (-1, 1)]
        }
    offsets = dir_offsets[direction]

    for i in range(3):
            for j in range(3):
                dy, dx = offsets[i * 3 + j]
                new_y, new_x = pos[0] + dy, pos[1] + dx
                
                if i == 1 and j == 1:  
                    sensor_matrix[i][j] = direction
                elif (0 <= new_y < len(self.maze) and 
                      0 <= new_x < len(self.maze[0])):
                    sensor_matrix[i][j] = self.maze[new_y][new_x]
                else:
                    sensor_matrix[i][j] = 'X' 
        
                return sensor_matrix # type: ignore

    def set_direction(self,direction):
        self.agent_direction = direction
    
    def move (self):
        return self.move_agent(self.agent_direction)
    
    def move_agent(self, direction):
        self.agent_direction = direction
        moves = {'N': (-1, 0), 'S': (1, 0), 'L': (0, 1), 'O': (0, -1)}
        dy, dx = moves[direction]
        
        new_x =self.agent_pos[0] + dx
        new_y = self.agent_pos[0] +dy

        if (0<= new_x < len(self.maze and 0 <= new_y < len(self.maze[0] and self.maze[new_y][new_x])) != 'X'):

            self.agent_pos = (new_y, new_x)
            self.steps += 1
            return True
        return False
    
    def get_current_cel(self):
        return self.maze[self.agent_pos[0]][self.agent_pos[1]] == 'S'
    
    def print_maze(self):
        direction_symbols = {'N': '↑', 'S': '↓', 'L': '→', 'O': '←'}

        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if (i, j) == self.agent_pos:
                    print(direction_symbols.get (self.agent_direction, 'A'), end = '')
                
                else:
                    print(cell, end='')
                print()
            print()

class Agent:
    def __init__(self, total_food):
        self.total_food = total_food
        self.collected_food = 0
        self.direction = 'N'
        self.memory = {}
        self.visited = set()
        self.path_history = []
        self.food_locations = set()
        self.exit_location = None

    def get_sensor(self):
        pass

    def set_direction(self,direction):
        self.direction = direction

    def move (self):
        pass

    def update_memory(self, sensor_data, current_pos):
          directions = ['N', 'S', 'L', 'O']
    dir_offsets = {
            'N': [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),  (0, 0),  (0, 1),
                  (1, -1),  (1, 0),  (1, 1)],
            'S': [(1, 1),   (1, 0),   (1, -1),
                  (0, 1),   (0, 0),   (0, -1),
                  (-1, 1),  (-1, 0),  (-1, -1)],
            'L': [(-1, 1),  (0, 1),   (1, 1),
                  (-1, 0),  (0, 0),   (1, 0),
                  (-1, -1), (0, -1),  (1, -1)],
            'O': [(1, -1),  (0, -1),  (-1, -1),
                  (1, 0),   (0, 0),   (-1, 0),
                  (1, 1),   (0, 1),   (-1, 1)]
        }
    offsets = dir_offsets[self.direction]

    for i in range (3):
        for j in range(3):
            dy, dx = offsets[i * 3 + j]
            map_pos = (current_pos[0] + dy, current_pos[1] + dx)
            cell_value = sensor_data [i][j]

            if i == 1 and j == 1:
                self.memory[map_pos] = '_'
            elif cell_value not in directions:
                self.memory[map_pos] = cell_value

                if cell_value == '0':
                    self.food_locations.add(map_pos)
                elif cell_value == 'S':
                    self.exit_locations = map_pos
    
    self.visited.add(current_pos)

