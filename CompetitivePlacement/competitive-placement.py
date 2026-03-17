import time
from random import randint
import networkx as nx
import matplotlib.pyplot as plt

def generate_graph_space(n_zones = 10):
    graph = {}
    for i in range(n_zones):
        graph[i] = []
    
    for i in range(n_zones):
        graph[i].append((i + 1) % n_zones)
        graph[(i + 1) % n_zones].append(i)

    return graph

def visualize_final_graph(graph, zone_values, occupied):
    G = nx.Graph()
    for zone in graph:
        G.add_node(zone, value=zone_values[zone])

    for zone, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(zone, neighbor)

    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(G, seed=42, k=2, iterations=50)

    colors = []
    for zone in G.nodes():
        if occupied[zone] == 0:
            colors.append('lightgray')
        elif occupied[zone] == 1:
            colors.append('lightblue')
        else:
            colors.append('lightcoral')

    node_sizes = [zone_values[zone] * 30 for zone in G.nodes()]

    nodes = nx.draw_networkx_nodes(G, pos, node_color=colors, node_size = node_sizes, alpha=0.9)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray')

    labels = {}
    for zone in G.nodes():
        owner = ""
        if occupied[zone] == 1:
            owner = "P1"
        elif occupied[zone] == 2:
            owner = "P2"
        labels[zone] = f"{zone}\n({zone_values[zone]})\n{owner}"
    
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')

    p1_score = sum(zone_values[z] for z in range(len(occupied)) if occupied[z] == 1)
    p2_score = sum(zone_values[z] for z in range(len(occupied)) if occupied[z] == 2)
    
    plt.title(f"Финальное состояние графа\nP1: {p1_score} очков | P2: {p2_score} очков", 
              fontsize=14, fontweight='bold')

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightgray', label='Свободна'),
        Patch(facecolor='lightblue', label='P1'),
        Patch(facecolor='lightcoral', label='P2')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def initialize_game(n_zones=2):
    graph = generate_graph_space(n_zones)
    zone_values = [randint(1, 100) for _ in range(n_zones)]
    occupied = [0] * n_zones  # 0 - свободна, 1 - P1, 2 - P2

    print(f"Количество зон: {n_zones}")
    print("Зона | Ценность | Соседи")
    print("-" * 30)
    for zone in range(n_zones):
        print(f"  {zone:2d}  |    {zone_values[zone]:3d}    | {graph[zone]}")
    
    return graph, zone_values, occupied

def is_zone_available(zone, graph, occupied):
    """Проверяет, может ли игрок занять зону"""
    if occupied[zone] != 0:
        return False
    
    for neighbor in graph[zone]:
        if occupied[neighbor] != 0:
            return False
    
    return True

def get_available_zones(graph, occupied):
    """Возвращает список доступных зон"""
    return [zone for zone in range(len(graph)) 
            if is_zone_available(zone, graph, occupied)]

def evaluate_zone(zone, zone_values, graph, occupied, player):
    """Оценивает ценность зоны для игрока"""
    score = zone_values[zone]
    
    # Для P2 добавляем бонус за блокировку ценных зон
    if player == 2:
        for neighbor in graph[zone]:
            if occupied[neighbor] == 0 and zone_values[neighbor] > 50:
                score += zone_values[neighbor] * 0.3
    
    return score

def find_best_move(graph, zone_values, occupied, player):
    available = get_available_zones(graph, occupied)
    
    if not available:
        return None, 0
    
    best_zone = None
    best_score = -1
    
    for zone in available:
        score = evaluate_zone(zone, zone_values, graph, occupied, player)
        if score > best_score:
            best_score = score
            best_zone = zone
    
    return best_zone, zone_values[best_zone]

def play_game(n_zones=10, max_moves_per_player=4, target_B=None):
    """Основная функция игры"""
    graph, zone_values, occupied = initialize_game(n_zones)
    
    players = [1, 2]
    current = 0
    scores = {1: 0, 2: 0}
    moves = 0
    total_moves = max_moves_per_player * 2

    if target_B:
        print(f"Цель для P2: набрать ≥ {target_B}")
    
    while moves < total_moves:
        player = players[current]
        zone, value = find_best_move(graph, zone_values, occupied, player)
        
        if zone is None:
            print(f"У игрока P{player} нет ходов!")
            break
        
        occupied[zone] = player
        scores[player] += value
        print(f"\nХод {moves+1}: P{player} → зона {zone} (ценность {value})")
        print(f"Счет: P1={scores[1]}, P2={scores[2]}")
        
        current = (current + 1) % 2
        moves += 1

    print(f"P1: {scores[1]} очков")
    print(f"P2: {scores[2]} очков")
    
    if target_B and scores[2] >= target_B:
        print(f"P2 достиг цели {target_B}")
    elif target_B:
        print(f"P2 не достиг цели {target_B}")
    
    if scores[1] > scores[2]:
        print("Победитель: P1")
    elif scores[2] > scores[1]:
        print("Победитель: P2")
    else:
        print("Ничья")
        
    print("\nОтрисовка финального графа...")
    visualize_final_graph(graph, zone_values, occupied)
    
    return scores[1], scores[2]

if __name__ == "__main__":
    start = time.time()
    play_game(n_zones=10, max_moves_per_player = 4, target_B = 200)
    end = time.time()
    print(f"\nВремя выполнения: {end - start:.3f} сек")