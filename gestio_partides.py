import random

def generar_calendari_lliga(participants):
    """
    Genera un calendari de lliga dividit en jornades.
    Cada jugador juga una vegada per jornada. Si queda un jugador sol, descansa.
    """
    if len(participants) % 2 != 0:
        participants.append("Descansa")  # Afegir un participant fictici si el número és imparell

    num_jornades = len(participants) - 1
    jornades = []

    for i in range(num_jornades):
        jornada = []
        for j in range(len(participants) // 2):
            jugador1 = participants[j]
            jugador2 = participants[-(j + 1)]
            jornada.append((jugador1, jugador2))
        jornades.append(jornada)
        # Rotar els participants per generar la següent jornada
        participants = [participants[0]] + [participants[-1]] + participants[1:-1]
    
    return jornades

def simular_partides_jornada(jornada, puntuacions):
    """
    Simula les partides d'una jornada i actualitza les puntuacions.
    """
    resultats = []
    for partida in jornada:
        jugador1, jugador2 = partida
        # Asegurarse de que ambos jugadores están en el diccionario de puntuaciones
        if jugador1 not in puntuacions:
            puntuacions[jugador1] = 0
        if jugador2 not in puntuacions:
            puntuacions[jugador2] = 0

        # Simular el ganador
        guanyador = jugador1 if jugador2 == "Bye" else random.choice([jugador1, jugador2])
        puntuacions[guanyador] += 1
        resultats.append((jugador1, jugador2, guanyador))
    return resultats

def generar_calendari_eliminatories(participants):
    rondes = []
    actuals = participants.copy()
    random.shuffle(actuals)
    
    # Si el número de participants és imparell, afegir un "bye"
    if len(actuals) % 2 != 0:
        actuals.append("Bye")  # Participant fictici

    while len(actuals) > 1:
        ronda = []
        for i in range(0, len(actuals), 2):
            ronda.append((actuals[i], actuals[i+1]))
        rondes.append(ronda)
        # Els guanyadors passen a la següent ronda
        actuals = [random.choice(partida) for partida in ronda if "Bye" not in partida]
    return rondes

def simular_partides(calendari, puntuacions):
    resultats = []
    for partida in calendari:
        jugador1, jugador2 = partida
        guanyador = random.choice([jugador1, jugador2])
        puntuacions[guanyador] += 1  
        resultats.append((jugador1, jugador2, guanyador))
    return resultats

def inicialitzar_puntuacions(participants):
    """
    Inicialitza el diccionari de puntuacions amb tots els participants a 0 punts.
    """
    return {participant: 0 for participant in participants}

def gestionar_torneig(participants, tipus_competicio):
    """
    Gestiona el torneig segons el tipus de competició (lliga o eliminatòries).
    """
    puntuacions = inicialitzar_puntuacions(participants)
    
    if tipus_competicio == "lliga":
        calendari = generar_calendari_lliga(participants)
        resultats = simular_partides(calendari, puntuacions)
        return resultats, puntuacions
    
    elif tipus_competicio == "eliminatories":
        resultats = []
        actuals = participants.copy()
        random.shuffle(actuals)
        
        # Si el número de participants és imparell, afegir un "descansa"
        if len(actuals) % 2 != 0:
            actuals.append("Descansa")  # Participant fictici
        
        while len(actuals) > 1:
            ronda_resultats = []
            nous_guanyadors = []
            for i in range(0, len(actuals), 2):
                jugador1 = actuals[i]
                jugador2 = actuals[i + 1]
                
                # Si un jugador és "Bye", l'altre passa automàticament
                if jugador1 == "Descansa":
                    guanyador = jugador2
                elif jugador2 == "Descansa":
                    guanyador = jugador1
                else:
                    guanyador = random.choice([jugador1, jugador2])
                
                ronda_resultats.append((jugador1, jugador2, guanyador))
                nous_guanyadors.append(guanyador)
            
            resultats.append(ronda_resultats)
            actuals = nous_guanyadors
            
            # Si el número de participants és imparell, afegir un "bye" per a la següent ronda
            if len(actuals) % 2 != 0 and len(actuals) > 1:
                actuals.append("Descansa")
        
        return resultats, {"Guanyador": actuals[0]}
    
    else:
        raise ValueError("Tipus de competició no vàlid. Tria 'lliga' o 'eliminatories'.")