def actualitzar_puntuacions(puntuacions, guanyador):
    if guanyador in puntuacions:
        puntuacions[guanyador] += 1
    else:
        puntuacions[guanyador] = 1

def calcular_ranquing(puntuacions):
    return sorted(puntuacions.items(), key=lambda x: x[1], reverse=True)