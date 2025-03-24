import os 
import re

def guardar_fitxer(nom_fitxer, dades):
    with open(nom_fitxer, 'w', encoding='utf-8') as f:
        for item in dades:
            f.write(f"{item}\n")

def carregar_fitxer(nom_fitxer):
    if os.path.exists(nom_fitxer):
        with open(nom_fitxer, 'r', encoding='utf-8') as f:
            return [linia.strip() for linia in f.readlines()]
    return []

def validar_nom_participant(nom):
    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ]+( [A-Za-zÀ-ÖØ-öø-ÿ]+)*$'
    return re.fullmatch(pattern, nom.strip()) is not None