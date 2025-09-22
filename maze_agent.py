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