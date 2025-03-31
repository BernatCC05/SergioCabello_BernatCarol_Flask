def inicialitzar_puntuacions(participants):
    return {participant: 0 for participant in participants}

def generar_ranquing(puntuacions, tipus_competicio):
    if tipus_competicio == "eliminatories":
        # Buscar el guanyador final
        guanyador = next((participant for participant, dades in puntuacions.items() if dades.get("estat") == "Guanyador"), None)
        if guanyador:
            return [f"Guanyador: {guanyador}"]
        else:
            return ["Encara no hi ha un guanyador."]
    elif tipus_competicio == "lliga":
        # Ordenar por puntuaciones numéricas
        ranquing = sorted(puntuacions.items(), key=lambda x: x[1], reverse=True)
        return [f"{participant}: {punts} punts" for participant, punts in ranquing]
    else:
        return []