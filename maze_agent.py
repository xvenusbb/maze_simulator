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
        
        