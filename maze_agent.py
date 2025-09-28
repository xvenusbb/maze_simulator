import copy
import time
import argparse

# ...demais definições de classes e funções...

def simular_labirinto(agente, ambiente, setas):
    # Backups do estado
    pos_backup = agente.pos
    dir_backup = agente.direcao
    passo_backup = agente.passo
    recompensa_backup = agente.recompensa_total
    comidas_coletadas_backup = agente.comidas_coletadas
    memoria_comidas_backup = agente.memoria_comidas
    grid_backup = copy.deepcopy(ambiente.grid)
    posicoes_comidas_backup = copy.deepcopy(ambiente.posicoes_comidas)
    try:
        while True:
            # Cria grid visual
            grid_vis = copy.deepcopy(ambiente.grid)
            for pos in ambiente.posicoes_comidas:
                grid_vis[pos[0]][pos[1]] = 'o'
            if ambiente.pos_saida:
                grid_vis[ambiente.pos_saida[0]][ambiente.pos_saida[1]] = 'S'
            i, j = agente.pos
            grid_vis[i][j] = setas[agente.direcao]
            print("Labirinto (X=pard, _=corr, o=comida, S=saída, ^/v/>/< = agente):")
            for row in grid_vis:
                print(''.join(row))
            print(f"Passo: {agente.passo}, Comidas: {agente.comidas_coletadas}/{agente.total_comidas}, "
                  f"Recompensa: {agente.recompensa_total}, Dir: {agente.direcao}")
            # Executa ação
            acao = agente.decidir_acao()
            if acao == 'move':
                agente.move()
            agente._atualizar_memoria_from_sensor()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nAnimação interrompida.")
    finally:
        # Restaura estado da simulação principal
        agente.pos = pos_backup
        agente.direcao = dir_backup
        agente.passo = passo_backup
        agente.recompensa_total = recompensa_backup
        agente.comidas_coletadas = comidas_coletadas_backup
        agente.memoria_comidas = memoria_comidas_backup
        ambiente.grid = grid_backup
        ambiente.posicoes_comidas = posicoes_comidas_backup

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulador de Agente em Labirinto")
    parser.add_argument("--arquivo", required=True,
                        help="Caminho para o arquivo TXT do labirinto")
    # ...restante do código principal...
   