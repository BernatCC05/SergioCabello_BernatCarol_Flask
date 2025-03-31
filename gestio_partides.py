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
    """
    Genera un calendari d'eliminatòries dividit en rondes.
    Cada ronda té partides entre dos participants. Si queda un jugador sol, descansa.
    """
    rondes = []
    actuals = participants.copy()
    random.shuffle(actuals)
    
    # Si el número de participants és imparell, afegir un "Descans"
    if len(actuals) % 2 != 0:
        actuals.append("Descans")  # Participant fictici

    while len(actuals) > 1:
        ronda = []
        for i in range(0, len(actuals), 2):
            # Comprovar que hi ha un segon jugador disponible
            if i + 1 < len(actuals):
                ronda.append((actuals[i], actuals[i + 1]))
            else:
                ronda.append((actuals[i], "Descans"))  # Afegir un "Descans" si falta un jugador
        rondes.append(ronda)
        # Els guanyadors passen a la següent ronda
        actuals = []
        for partida in ronda:
            jugador1, jugador2 = partida
            if jugador2 == "Descans":
                actuals.append(jugador1)  # El jugador sense rival passa automàticament
            else:
                actuals.append(random.choice([jugador1, jugador2]))  # Simular el guanyador
    return rondes

def simular_partides(calendari, puntuacions, tipus_competicio):
    """
    Simula les partides d'un calendari i actualitza les puntuacions segons el tipus de competició.
    """
    resultats = []
    for ronda in calendari:
        ronda_resultats = []
        for partida in ronda:
            jugador1, jugador2 = partida
            # Asegurarse de que ambos jugadores están en el diccionario de puntuaciones
            if jugador1 not in puntuacions:
                puntuacions[jugador1] = {"estat": "Participa", "victories": 0}
            if jugador2 not in puntuacions and jugador2 != "Descans":
                puntuacions[jugador2] = {"estat": "Participa", "victories": 0}

            # Simular el ganador
            if jugador2 == "Descans":
                guanyador = jugador1
            else:
                guanyador = random.choice([jugador1, jugador2])

            if tipus_competicio == "lliga":
                # En una lliga, sumar punts al guanyador
                puntuacions[guanyador] += 1
            elif tipus_competicio == "eliminatories":
                # En una eliminatòria, actualitzar l'estat del guanyador
                puntuacions[guanyador]["estat"] = "Avança"
                puntuacions[guanyador]["victories"] += 1
                if jugador2 != "Descans":
                    puntuacions[jugador2]["estat"] = "Eliminat"

            ronda_resultats.append((jugador1, jugador2, guanyador))
        resultats.append(ronda_resultats)

    # Marcar el guanyador final si només queda un jugador
    if tipus_competicio == "eliminatories" and len(puntuacions) > 0:
        guanyador_final = max(puntuacions.items(), key=lambda x: x[1]["victories"] if x[1]["estat"] == "Avança" else 0)
        puntuacions[guanyador_final[0]]["estat"] = "Guanyador"

    return resultats

def inicialitzar_puntuacions(participants, tipus_competicio):
    """
    Inicialitza el diccionari de puntuacions segons el tipus de competició.
    """
    if tipus_competicio == "lliga":
        # En una lliga, les puntuacions són punts acumulats
        return {participant: 0 for participant in participants}
    elif tipus_competicio == "eliminatories":
        # En una eliminatòria, les puntuacions reflecteixen el progrés
        return {participant: {"estat": "Participa"} for participant in participants}
    else:
        raise ValueError("Tipus de competició no vàlid. Tria 'lliga' o 'eliminatories'.")

def gestionar_torneig(participants, tipus_competicio):
    """
    Gestiona el torneig segons el tipus de competició (lliga o eliminatòries).
    """
    puntuacions = inicialitzar_puntuacions(participants, tipus_competicio)
    
    if tipus_competicio == "lliga":
        calendari = generar_calendari_lliga(participants)
        resultats = simular_partides(calendari, puntuacions, tipus_competicio)
        return resultats, puntuacions
    
    elif tipus_competicio == "eliminatories":
        # Generar el calendari d'eliminatòries
        calendari = generar_calendari_eliminatories(participants)
        resultats = simular_partides(calendari, puntuacions, tipus_competicio)
        
        # Obtenir el guanyador final
        guanyador = None
        if calendari and calendari[-1]:  # Comprovar que hi ha una última ronda
            ultima_ronda = calendari[-1]
            if len(ultima_ronda) == 1:  # L'última ronda ha de tenir només una partida
                guanyador = ultima_ronda[0][0] if ultima_ronda[0][1] == "Descans" else ultima_ronda[0][2]
                puntuacions[guanyador]["estat"] = "Guanyador"

        return resultats, puntuacions
    
    else:
        raise ValueError("Tipus de competició no vàlid. Tria 'lliga' o 'eliminatories'.")