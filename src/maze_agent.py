import sys
import os
import random
import time
from collections import deque

# --- CONFIGURAÇÃO ---
NOME_ARQUIVO_PADRAO = "maze.txt"
ATRASO_VISUALIZACAO = 0.05 # Pausa em segundos entre os passos

class Ambiente:
    def __init__(self, nome_arquivo):
        self.labirinto = []
        self.labirinto_base = [] # Para checar a saida 'S' no local original
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
        """Carrega labirinto do arquivo de texto"""
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.read().strip().split('\n')

        # Normaliza comprimento de linhas (se houver variação) - pega o maior
        self.linhas = len(linhas)
        self.colunas = max(len(l) for l in linhas) if linhas else 0

        # Preenche cada linha para o mesmo tamanho (com X se faltar)
        self.labirinto = [list(l.ljust(self.colunas, 'X')) for l in linhas]
        # Cria uma cópia imutável do mapa original (útil para saída 'S')
        self.labirinto_base = [list(l) for l in self.labirinto]

    def encontrar_posicao_agente(self):
        """Encontra posição inicial do agente (E)"""
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.labirinto[i][j] == 'E':
                    self.linha_agente = i
                    self.coluna_agente = j
                    self.direcao_agente = 'N'  # Direção padrão
                    self.labirinto[i][j] = '_'  # Substitui entrada por corredor
                    return

    def contar_comida(self):
        """Conta total de comida no labirinto"""
        self.total_comida = 0
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.labirinto[i][j] == 'o':
                    self.total_comida += 1
        self.comida_restante = self.total_comida

    def obter_sensor(self):
        """Retorna matriz 3x3 do sensor ao redor do agente"""
        sensor = [['X' for _ in range(3)] for _ in range(3)]

        # Obtém área 3x3 ao redor do agente
        for i in range(3):
            for j in range(3):
                linha = self.linha_agente - 1 + i
                coluna = self.coluna_agente - 1 + j

                # Verifica limites
                if linha < 0 or linha >= self.linhas or coluna < 0 or coluna >= self.colunas:
                    sensor[i][j] = 'X'  # Parede para fora dos limites
                else:
                    # Usa o labirinto modificável, mas checa a saída no base
                    if self.labirinto_base[linha][coluna] == 'S':
                        sensor[i][j] = 'S'
                    else:
                        sensor[i][j] = self.labirinto[linha][coluna]

        # O centro (1,1) é a posição do agente no sensor
        # O agente não precisa do seu próprio conteúdo, ele usa a direção, mas vamos manter o '_' ou 'o'
        # O código original usava a direção, mas isso não é o conteúdo do mapa:
        # sensor[1][1] = self.direcao_agente 
        
        # Deixamos o agente no centro como a direção para a lógica dele
        sensor[1][1] = self.direcao_agente

        return sensor

    def definir_direcao(self, direcao):
        """Define direção do agente"""
        self.direcao_agente = direcao

    def mover(self):
        """
        Move agente na direção atual.
        Retorna (moveu_sucesso, coletou_comida)
        """
        nova_linha = self.linha_agente
        nova_coluna = self.coluna_agente

        # Calcula nova posição baseada na direção
        if self.direcao_agente == 'N':
            nova_linha -= 1
        elif self.direcao_agente == 'S':
            nova_linha += 1
        elif self.direcao_agente == 'L':
            nova_coluna += 1
        elif self.direcao_agente == 'O':
            nova_coluna -= 1
            
        coletou_comida = False
        
        # Verifica se movimento é válido e não é parede
        if (0 <= nova_linha < self.linhas and 
            0 <= nova_coluna < self.colunas and
            self.labirinto_base[nova_linha][nova_coluna] != 'X' and
            self.labirinto[nova_linha][nova_coluna] != 'X'):
            
            # Checa o conteúdo da nova posição no mapa jogável
            conteudo_destino = self.labirinto[nova_linha][nova_coluna]
            
            # Verifica se há comida na nova posição
            if conteudo_destino == 'o':
                self.comida_restante -= 1
                self.labirinto[nova_linha][nova_coluna] = '_'  # Come a comida
                coletou_comida = True

            self.linha_agente = nova_linha
            self.coluna_agente = nova_coluna
            
            return True, coletou_comida

        return False, coletou_comida  # Movimento inválido

    def esta_na_saida(self):
        """Verifica se agente está na saída"""
        # Checa a saida no mapa base, pois ela não é alterada no mapa jogável
        return self.labirinto_base[self.linha_agente][self.coluna_agente] == 'S'

    def toda_comida_coletada(self):
        """Verifica se toda comida foi coletada"""
        return self.comida_restante == 0

    def obter_total_comida(self):
        """Obtém contagem total de comida"""
        return self.total_comida

    def obter_comida_restante(self):
        """Obtém contagem de comida restante"""
        return self.comida_restante

    def imprimir_labirinto(self):
        """Imprime estado atual do labirinto com posição do agente (com flush e clear)"""
        # Limpa o console para simular a animação (Crucial para o efeito de "passagem")
        os.system('cls' if os.name == 'nt' else 'clear') 
        
        linhas = []
        for i in range(self.linhas):
            linha_chars = []
            for j in range(self.colunas):
                if i == self.linha_agente and j == self.coluna_agente:
                    linha_chars.append('A')  # Mostra posição do agente
                elif self.labirinto_base[i][j] == 'S':
                    linha_chars.append('S') # Garante que a saída sempre apareça
                else:
                    linha_chars.append(self.labirinto[i][j])
            linhas.append(''.join(linha_chars))
            
        # Imprime tudo de uma vez e força flush para evitar buffering
        print('\n'.join(linhas), flush=True)
        # O '\n' extra do código original: print(flush=True)
        print(flush=True)


class Agente:
    def __init__(self, ambiente, comida_esperada):
        self.ambiente = ambiente
        self.comida_esperada = comida_esperada
        self.passos = 0                # Contador de movimentos efetivos
        self.comida_coletada = 0
        self.posicoes_visitadas = set()
        self.direcoes = ['N', 'L', 'S', 'O']  # Norte, Leste, Sul, Oeste
        self.modo_detalhado = True 

        # Sistema de memória
        self.mapa_conhecido = {}  
        self.contador_visitas = {}  
        self.locais_comida = set()  
        self.posicoes_exploradas = set() 
        self.caminho_cache = deque() # Armazena o caminho pré-calculado

        # Contador de iterações (inclui tentativas – útil para acompanhar passo-a-passo)
        self.iteracoes = 0
        
        # Inicia a contagem de visitas na posição inicial
        self.contador_visitas[self.obter_posicao_atual()] = 1

    def executar(self):
        """Loop principal de execução do agente (imprime passo-a-passo desde o início)"""
        print("Agente iniciou exploração!", flush=True)
        print("Passo 0 (inicial):", flush=True)
        self.ambiente.imprimir_labirinto()

        # Continua até que TODA comida tenha sido coletada E o agente esteja na saída
        while not (self.ambiente.toda_comida_coletada() and self.ambiente.esta_na_saida()):
            self.iteracoes += 1
            
            # --- Início do passo ---
            sensor = self.ambiente.obter_sensor()
            self.atualizar_memoria(sensor) # Atualiza mapa interno com dados do sensor

            # Decisão de movimento
            proxima_direcao = self.decidir_proximo_movimento(sensor)
            self.ambiente.definir_direcao(proxima_direcao)

            # Log da tentativa antes de executar
            print(f"Iteração {self.iteracoes} — Tentativa de mover: {proxima_direcao} (Passos efetivos: {self.passos})", flush=True)

            # Execução do movimento
            moveu, coletou_comida = self.ambiente.mover()

            # --- Após o passo ---
            if moveu:
                self.passos += 1
                # Rastreia posição atual
                posicao_atual = self.obter_posicao_atual()
                # Remove o passo do cache, pois foi executado com sucesso
                if self.caminho_cache:
                    self.caminho_cache.popleft()
                    
                self.contador_visitas[posicao_atual] = self.contador_visitas.get(posicao_atual, 0) + 1

                if coletou_comida:
                    self.comida_coletada += 1
                    print(f"Comida coletada! Total: {self.comida_coletada}", flush=True)
                    # Remove comida da memória já que foi coletada
                    if posicao_atual in self.locais_comida:
                        self.locais_comida.remove(posicao_atual)
            else:
                print("Movimento bloqueado (parede/limite).", flush=True)
                # Se bateu, limpa o cache para recalcular
                self.caminho_cache.clear()

            # Imprime o labirinto a cada iteração
            print(f"-- Estado após iteração {self.iteracoes} (passos efetivos: {self.passos}) --", flush=True)
            self.ambiente.imprimir_labirinto()

            # Pausa para visualização
            if self.modo_detalhado:
                time.sleep(ATRASO_VISUALIZACAO)

            # Previne loops infinitos
            if self.iteracoes > 20000:
                print("Número máximo de iterações atingido! Interrompendo.", flush=True)
                break

        self.imprimir_resultados_finais()

    def atualizar_memoria(self, sensor):
        """Atualiza mapa interno baseado nos dados do sensor"""
        posicao_atual = self.obter_posicao_atual()

        # Atualiza conhecimento da área circundante
        for i in range(3):
            for j in range(3):
                # Calcula posição real no labirinto
                linha = posicao_atual[0] + (i - 1)
                coluna = posicao_atual[1] + (j - 1)
                pos = (linha, coluna)

                # Pula posição central (posição do agente, que é a direção no sensor)
                if i == 1 and j == 1:
                    continue

                conteudo_celula = sensor[i][j]

                # Atualiza nosso mapa
                self.mapa_conhecido[pos] = conteudo_celula

                # Rastreia locais de comida
                if conteudo_celula == 'o':
                    self.locais_comida.add(pos)
                elif pos in self.locais_comida and conteudo_celula != 'o':
                    # Comida foi coletada, remove dos locais conhecidos
                    self.locais_comida.discard(pos) # .discard() é seguro se o elemento não existir
                    
    def obter_posicao_atual(self):
        """Obtém posição atual do agente do ambiente"""
        return (self.ambiente.linha_agente, self.ambiente.coluna_agente)

    def _encontrar_caminho_bfs(self, alvo_char, inicio=None):
        """Busca em Largura (BFS) na memória para encontrar o caminho até o alvo."""
        inicio = inicio if inicio else self.obter_posicao_atual()
        
        alvos_candidatos = [pos for pos, char in self.mapa_conhecido.items() if char == alvo_char]
        
        if not alvos_candidatos:
            return None, None 

        fila = deque([(inicio, [])])  # (posição, caminho_de_direções)
        visitados_bfs = {inicio}
        
        direcoes_map = {'N': (-1, 0), 'L': (0, 1), 'S': (1, 0), 'O': (0, -1)}
        
        while fila:
            (r, c), caminho = fila.popleft()
            
            if (r, c) in alvos_candidatos:
                return caminho, (r, c) # Caminho para o alvo mais próximo encontrado

            for dir_char, (dr, dc) in direcoes_map.items():
                prox_r, prox_c = r + dr, c + dc
                prox_pos = (prox_r, prox_c)
                
                # Checa se a posição está na memória, não é parede 'X' e não foi visitada
                if prox_pos in self.mapa_conhecido and prox_pos not in visitados_bfs:
                    if self.mapa_conhecido[prox_pos] != 'X':
                        visitados_bfs.add(prox_pos)
                        fila.append((prox_pos, caminho + [dir_char]))
        
        return None, None 

    def decidir_proximo_movimento(self, sensor):
        """Decide próximo movimento baseado no sensor, memória e cache BFS"""
        
        # 1. Se o cache de caminho estiver vazio, encontre um novo caminho
        if not self.caminho_cache:
            
            # Prioridade A: Coletar toda a comida
            if not self.ambiente.toda_comida_coletada():
                caminho, _ = self._encontrar_caminho_bfs('o')
                if caminho:
                    self.caminho_cache = deque(caminho)
            
            # Prioridade B: Ir para a saída (só se toda a comida foi coletada)
            elif self.ambiente.toda_comida_coletada() and not self.ambiente.esta_na_saida():
                caminho, _ = self._encontrar_caminho_bfs('S')
                if caminho:
                    self.caminho_cache = deque(caminho)
            
        # 2. Executar caminho em cache (se existir)
        if self.caminho_cache:
            return self.caminho_cache[0]

        # 3. Exploração (Nenhum alvo ou caminho bloqueado)
        posicao_atual = self.obter_posicao_atual()
        
        direcoes_disponiveis = []
        posicoes_direcoes = {
            'N': (posicao_atual[0] - 1, posicao_atual[1]),
            'L': (posicao_atual[0], posicao_atual[1] + 1),
            'S': (posicao_atual[0] + 1, posicao_atual[1]),
            'O': (posicao_atual[0], posicao_atual[1] - 1)
        }

        for direcao, proxima_pos in posicoes_direcoes.items():
            if self.pode_mover_na_direcao(sensor, direcao):
                # Prefere posições menos visitadas
                contador_visitas = self.contador_visitas.get(proxima_pos, 0)
                direcoes_disponiveis.append((direcao, contador_visitas))

        if direcoes_disponiveis:
            # Ordena por contador de visitas (prefere posições menos visitadas)
            direcoes_disponiveis.sort(key=lambda x: x[1])
            # Retorna a direção menos visitada
            return direcoes_disponiveis[0][0]

        # 4. Último recurso: Travado, tenta direção atual
        return self.ambiente.direcao_agente 

    def pode_mover_na_direcao(self, sensor, direcao):
        """Verifica se agente pode mover na direção dada"""
        mapa_direcoes = {
            'N': sensor[0][1],
            'L': sensor[1][2],
            'S': sensor[2][1],
            'O': sensor[1][0]
        }
        # Não pode mover se for parede 'X'
        return mapa_direcoes.get(direcao, 'X') != 'X'

    def imprimir_resultados_finais(self):
        """Imprime resultados finais e pontuação"""
        print("\n=== RESULTADOS FINAIS ===", flush=True)
        print(f"Passos dados: {self.passos}", flush=True)
        print(f"Comida coletada: {self.comida_coletada}", flush=True)
        print(f"Comida esperada: {self.comida_esperada}", flush=True)

        pontos_comida = self.comida_coletada * 10
        penalidade_passos = self.passos * 1
        pontuacao_total = pontos_comida - penalidade_passos

        print("\n=== PONTUAÇÃO ===", flush=True)
        print(f"Pontos por comida (10 por comida): {pontos_comida}", flush=True)
        print(f"Penalidade por passos (-1 por passo): -{penalidade_passos}", flush=True)
        print(f"PONTUAÇÃO TOTAL: {pontuacao_total}", flush=True)

        if self.ambiente.toda_comida_coletada() and self.ambiente.esta_na_saida():
            print("SUCESSO: Toda comida coletada e chegou na saída!", flush=True)
        elif self.ambiente.toda_comida_coletada():
            print("Sucesso parcial: Toda comida coletada mas não chegou na saída", flush=True)
        else:
            restante = self.ambiente.obter_comida_restante()
            print(f"Missão incompleta: {restante} comida restante", flush=True)


def criar_labirinto_exemplo():
    """Cria um arquivo de labirinto exemplo para teste"""
    # Exemplo criado para ser resolvível
    labirinto_exemplo = """XXXXXXXXX
XE______X
X_XXXX_oX
X_o____XX
XXX_X___X
X_o___X_X
X_XXX_X_X
X_____o_X
XXXXXXSXX"""

    with open(NOME_ARQUIVO_PADRAO, "w") as f:
        f.write(labirinto_exemplo)


def main():
    try:
        # Verifica se nome do arquivo foi fornecido como argumento
        nome_arquivo = NOME_ARQUIVO_PADRAO
        modo_detalhado = True

        if len(sys.argv) > 1:
            nome_arquivo = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == "simples":
            modo_detalhado = False

        print(f"Carregando labirinto de: {nome_arquivo}", flush=True)

        # Verifica se arquivo existe
        if not os.path.exists(nome_arquivo):
            print(f"Erro: Arquivo '{nome_arquivo}' não encontrado!", flush=True)
            print(f"\nCriando arquivo de exemplo {NOME_ARQUIVO_PADRAO}...", flush=True)
            criar_labirinto_exemplo()
            print(f"Arquivo {NOME_ARQUIVO_PADRAO} criado! Execute o programa novamente.", flush=True)
            return

        # Cria ambiente
        ambiente = Ambiente(nome_arquivo)

        # Obtém contagem total de comida
        total_comida = ambiente.obter_total_comida()
        print(f"Total de comida no labirinto: {total_comida}", flush=True)

        # Cria e executa agente
        agente = Agente(ambiente, total_comida)
        agente.modo_detalhado = modo_detalhado
        agente.executar()

    except FileNotFoundError:
        print(f"Erro: Não foi possível encontrar o arquivo do labirinto", flush=True)
        print("\nFormato do arquivo maze.txt:", flush=True)
        print("XXXXXXX", flush=True)
        print("XE__o_X", flush=True)
        # ... (instruções de formato omitidas por brevidade, mas o código as inclui)
    except Exception as e:
        print(f"Erro inesperado: {e}", flush=True)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
