import re

def validar_nom(nom):
    return bool(re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nom))