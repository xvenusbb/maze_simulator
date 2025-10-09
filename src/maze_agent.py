import sys
import os
import time
from collections import deque
import cv2
import numpy as np

NOME_ARQUIVO_PADRAO = "maze.txt"
ATRASO_VISUALIZACAO = 0.05
TAMANHO_CELULA = 40  # tamanho de cada célula no display OpenCV
NOME_JANELA = "Labirinto"

# Cores (BGR)
COR_FUNDO = (200, 200, 200)
COR_PAREDE = (50, 50, 50)
COR_COMIDA = (0, 165, 255)
COR_ENTRADA = (255, 0, 0)
COR_SAIDA = (0, 255, 0)
COR_AGENTE = (0, 0, 255)


class Ambiente:
    def __init__(self, nome_arquivo):
        self.labirinto = []
        self.labirinto_base = []
        self.linha_agente = 0
        self.coluna_agente = 0
        self.direcao_agente = 'N'
        self.linhas = 0
        self.colunas = 0
        self.total_comida = 0
        self.comida_restante = 0

        self.carregar_labirinto(nome_arquivo)
        self.encontrar_posicao_agente()
        self.contar_comida()

    def carregar_labirinto(self, nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.read().strip().split('\n')
        self.linhas = len(linhas)
        self.colunas = max(len(l) for l in linhas) if linhas else 0
        self.labirinto = [list(l.ljust(self.colunas, 'X')) for l in linhas]
        self.labirinto_base = [list(l) for l in self.labirinto]

    def encontrar_posicao_agente(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.labirinto[i][j] == 'E':
                    self.linha_agente = i
                    self.coluna_agente = j
                    self.direcao_agente = 'N'
                    self.labirinto[i][j] = '_'
                    return

    def contar_comida(self):
        self.total_comida = sum(self.labirinto[i][j] == 'o' for i in range(self.linhas) for j in range(self.colunas))
        self.comida_restante = self.total_comida

    def obter_sensor(self):
        sensor = [['X' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                linha = self.linha_agente - 1 + i
                coluna = self.coluna_agente - 1 + j
                if 0 <= linha < self.linhas and 0 <= coluna < self.colunas:
                    sensor[i][j] = self.labirinto[linha][coluna]
                    if self.labirinto_base[linha][coluna] == 'S':
                        sensor[i][j] = 'S'
        sensor[1][1] = self.direcao_agente
        return sensor

    def definir_direcao(self, direcao):
        self.direcao_agente = direcao

    def mover(self):
        nova_linha, nova_coluna = self.linha_agente, self.coluna_agente
        if self.direcao_agente == 'N': nova_linha -= 1
        elif self.direcao_agente == 'S': nova_linha += 1
        elif self.direcao_agente == 'L': nova_coluna += 1
        elif self.direcao_agente == 'O': nova_coluna -= 1

        coletou_comida = False

        if 0 <= nova_linha < self.linhas and 0 <= nova_coluna < self.colunas:
            if self.labirinto_base[nova_linha][nova_coluna] != 'X' and self.labirinto[nova_linha][nova_coluna] != 'X':
                if self.labirinto[nova_linha][nova_coluna] == 'o':
                    self.comida_restante -= 1
                    self.labirinto[nova_linha][nova_coluna] = '_'
                    coletou_comida = True
                self.linha_agente, self.coluna_agente = nova_linha, nova_coluna
                return True, coletou_comida

        return False, coletou_comida

    def esta_na_saida(self):
        return self.labirinto_base[self.linha_agente][self.coluna_agente] == 'S'

    def toda_comida_coletada(self):
        return self.comida_restante == 0

    def obter_total_comida(self):
        return self.total_comida

    def imprimir_labirinto(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        linhas = []
        for i in range(self.linhas):
            linha_chars = []
            for j in range(self.colunas):
                if i == self.linha_agente and j == self.coluna_agente:
                    linha_chars.append('A')
                elif self.labirinto_base[i][j] == 'S':
                    linha_chars.append('S')
                else:
                    linha_chars.append(self.labirinto[i][j])
            linhas.append(''.join(linha_chars))
        print('\n'.join(linhas), flush=True)


def criar_labirinto_exemplo():
    labirinto_exemplo = """XXXXXXXXX
XE_o__o_X
X_XXXX_oX
X_o__o_XX
X0_X_X_o_X
X_o___X_X
X_XXX_X_X
X_o__o_oS
XXXXXXXXX"""
    with open(NOME_ARQUIVO_PADRAO, "w") as f:
        f.write(labirinto_exemplo)


def criar_frame_labirinto(ambiente):
    frame = np.full((ambiente.linhas * TAMANHO_CELULA, ambiente.colunas * TAMANHO_CELULA, 3), COR_FUNDO, dtype=np.uint8)
    for i in range(ambiente.linhas):
        for j in range(ambiente.colunas):
            char = ambiente.labirinto[i][j]
            if i == ambiente.linha_agente and j == ambiente.coluna_agente:
                char = 'A'
            elif ambiente.labirinto_base[i][j] == 'S':
                char = 'S'
            x1, y1 = j * TAMANHO_CELULA, i * TAMANHO_CELULA
            x2, y2 = x1 + TAMANHO_CELULA, y1 + TAMANHO_CELULA
            cor = COR_FUNDO
            if char == 'X': cor = COR_PAREDE
            elif char == 'o': cor = COR_COMIDA
            elif char == 'A': cor = COR_AGENTE
            elif char == 'E': cor = COR_ENTRADA
            elif char == 'S': cor = COR_SAIDA
            cv2.rectangle(frame, (x1, y1), (x2, y2), cor, -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), COR_PAREDE, 1)
    return frame

def obter_comida_total(self):
        """Retorna todas as posições que ainda têm comida"""
        comida = []
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.labirinto[i][j] == 'o':
                    comida.append((i, j))
        return comida

class Agente:
    def __init__(self, ambiente, comida_esperada):
        self.ambiente = ambiente
        self.comida_esperada = comida_esperada
        self.passos = 0
        self.comida_coletada = 0
        self.contador_visitas = {}
        self.mapa_conhecido = {}
        self.locais_comida = set()
        self.caminho_cache = deque()
        self.iteracoes = 0

        self.contador_visitas[self.obter_posicao_atual()] = 1

    def obter_posicao_atual(self):
        return self.ambiente.linha_agente, self.ambiente.coluna_agente

    def atualizar_memoria(self, sensor):
        pos_atual = self.obter_posicao_atual()
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1: continue
                linha, coluna = pos_atual[0] + (i - 1), pos_atual[1] + (j - 1)
                if 0 <= linha < self.ambiente.linhas and 0 <= coluna < self.ambiente.colunas:
                    self.mapa_conhecido[(linha, coluna)] = sensor[i][j]
                    if sensor[i][j] == 'o':
                        self.locais_comida.add((linha, coluna))
                    elif (linha, coluna) in self.locais_comida and sensor[i][j] != 'o':
                        self.locais_comida.discard((linha, coluna))

    def _encontrar_caminho_bfs(self, alvo_char):
        inicio = self.obter_posicao_atual()
        alvos = [pos for pos, char in self.mapa_conhecido.items() if char == alvo_char]
        if not alvos: return None
        fila = deque([(inicio, [])])
        visitados = {inicio}
        direcoes_map = {'N': (-1, 0), 'S': (1, 0), 'L': (0, 1), 'O': (0, -1)}
        while fila:
            (r, c), caminho = fila.popleft()
            if (r, c) in alvos: return caminho
            for dir_char, (dr, dc) in direcoes_map.items():
                prox = (r + dr, c + dc)
                if prox in self.mapa_conhecido and prox not in visitados:
                    if self.mapa_conhecido[prox] != 'X':
                        visitados.add(prox)
                        fila.append((prox, caminho + [dir_char]))
        return None

    def decidir_proximo_movimento(self, sensor):
        if not self.caminho_cache:
            if not self.ambiente.toda_comida_coletada():
                caminho = self._encontrar_caminho_bfs('o')
            else:
                caminho = self._encontrar_caminho_bfs('S')
            if caminho: self.caminho_cache = deque(caminho)

        if self.caminho_cache:
            return self.caminho_cache[0]

        # fallback: mover para direção menos visitada
        pos = self.obter_posicao_atual()
        direcoes = {'N': (pos[0]-1,pos[1]), 'S': (pos[0]+1,pos[1]), 'L': (pos[0],pos[1]+1), 'O': (pos[0],pos[1]-1)}
        disponiveis = [(d, self.contador_visitas.get(p,0)) for d,p in direcoes.items() 
                       if 0<=p[0]<self.ambiente.linhas and 0<=p[1]<self.ambiente.colunas 
                       and self.ambiente.labirinto_base[p[0]][p[1]] != 'X']
        if disponiveis:
            disponiveis.sort(key=lambda x:x[1])
            return disponiveis[0][0]
        return self.ambiente.direcao_agente
    def executar(self):
        cv2.namedWindow(NOME_JANELA)
        while not (self.ambiente.toda_comida_coletada() and self.ambiente.esta_na_saida()):
            self.iteracoes += 1
            sensor = self.ambiente.obter_sensor()
            self.atualizar_memoria(sensor)
            direcao = self.decidir_proximo_movimento(sensor)
            self.ambiente.definir_direcao(direcao)
            moveu, coletou = self.ambiente.mover()
            if moveu:
                self.passos += 1
                pos = self.obter_posicao_atual()
                self.contador_visitas[pos] = self.contador_visitas.get(pos,0)+1
                if coletou:
                    self.comida_coletada +=1
                    if pos in self.locais_comida:
                        self.locais_comida.remove(pos)
                if self.caminho_cache:
                    self.caminho_cache.popleft()
            frame = criar_frame_labirinto(self.ambiente)
            cv2.imshow(NOME_JANELA, frame)
            if cv2.waitKey(int(ATRASO_VISUALIZACAO*1000)) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        print(f"Passos: {self.passos}, Comida coletada: {self.comida_coletada}/{self.comida_esperada}")
        print("Concluído!")


def main():
    if not os.path.exists(NOME_ARQUIVO_PADRAO):
        criar_labirinto_exemplo()
    ambiente = Ambiente(NOME_ARQUIVO_PADRAO)
    agente = Agente(ambiente, ambiente.obter_total_comida())
    agente.executar()

def usar_sensor_comida(self):
 """Recebe todas as posições de comida ainda no labirinto"""
 posicoes_comida = self.ambiente.obter_comida_total()
 self.locais_comida = set(posicoes_comida)


if __name__ == "__main__":
    main()
