import utils

def afegir_participant(nom):
    if utils.validar_nom(nom):
        return True
    return False

def desar_participants_a_fitxer(participants, fitxer):
    with open(fitxer, 'w') as f:
        for participant in participants:
            f.write(participant + '\n')

def carregar_participants_de_fitxer(fitxer):
    with open(fitxer, 'r') as f:
        return [line.strip() for line in f.readlines()]