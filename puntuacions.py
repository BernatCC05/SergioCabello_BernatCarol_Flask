def inicialitzar_puntuacions(participants):
    return {participant: 0 for participant in participants}

def generar_ranquing(puntuacions):
    return sorted(puntuacions.items(), key=lambda x: x[1], reverse=True)