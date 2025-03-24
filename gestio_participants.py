import re
import utils

def validar_nom_participant(nom):
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
    return re.fullmatch(pattern, nom.strip()) is not None

def afegir_participant(nom):
    participants = carregar_participants()
    nom_net = nom.strip()
    
    # Verificar duplicats
    if any(nom_net.lower() == p.lower() for p in participants):
        return "duplicat"
    
    # Afegir participant validat
    participants.append(nom_net)
    utils.guardar_fitxer('participants.txt', participants)
    return "ok"

def carregar_participants():
    return utils.carregar_fitxer('participants.txt')