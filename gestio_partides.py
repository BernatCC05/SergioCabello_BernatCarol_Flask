import random

def generar_calendari_lliga(participants):
    calendari = []
    for i in range(len(participants)):
        for j in range(i + 1, len(participants)):
            calendari.append((participants[i], participants[j]))
    return calendari

def generar_calendari_eliminatories(participants):
    rondes = []
    actuals = participants.copy()
    random.shuffle(actuals)
    
    while len(actuals) > 1:
        ronda = []
        for i in range(0, len(actuals), 2):
            ronda.append((actuals[i], actuals[i+1]))
        rondes.append(ronda)
        actuals = [f"Guanyador {i+1}" for i in range(len(ronda))]
    return rondes

def simular_partides(calendari, puntuacions):
    resultats = []
    for partida in calendari:
        jugador1, jugador2 = partida
        guanyador = random.choice([jugador1, jugador2])
        puntuacions[guanyador] += 1  
        resultats.append((jugador1, jugador2, guanyador))
    return resultats