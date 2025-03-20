import random

def generar_partides(participants):
    random.shuffle(participants)
    return [(participants[i], participants[i+1]) for i in range(0, len(participants)-1, 2)]

def desar_partides_a_fitxer(partides, fitxer):
    with open(fitxer, 'w') as f:
        for partida in partides:
            f.write(f"{partida[0]} vs {partida[1]}\n")

def carregar_partides_de_fitxer(fitxer):
    with open(fitxer, 'r') as f:
        return [tuple(line.strip().split(' vs ')) for line in f.readlines()]
    









