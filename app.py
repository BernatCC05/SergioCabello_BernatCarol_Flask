from flask import Flask, render_template, request, redirect, url_for, session, flash
import gestio_participants as gp
import gestio_partides as gpa
import puntuacions as punts
import utils
import random
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

import json

def guardar_estat_torneig():
    estat = {
        "participants": gp.carregar_participants(),
        "puntuacions": session.get('puntuacions', {}),
        "calendari_lliga": session.get('calendari_lliga', []),
        "jornada_actual": session.get('jornada_actual', 0),
        "calendari_eliminatories": session.get('calendari_eliminatories', []),
        "ronda_actual": session.get('ronda_actual', 0),
        "tipus_competicio": session.get('tipus_competicio', None)
    }
    with open('estat_torneig.json', 'w', encoding='utf-8') as f:
        json.dump(estat, f, ensure_ascii=False, indent=4)

def carregar_estat_torneig():
    if os.path.exists('estat_torneig.json'):
        with open('estat_torneig.json', 'r', encoding='utf-8') as f:
            estat = json.load(f)
        session['puntuacions'] = estat.get('puntuacions', {})
        session['calendari_lliga'] = estat.get('calendari_lliga', [])
        session['jornada_actual'] = estat.get('jornada_actual', 0)
        session['calendari_eliminatories'] = estat.get('calendari_eliminatories', [])
        session['ronda_actual'] = estat.get('ronda_actual', 0)
        session['tipus_competicio'] = estat.get('tipus_competicio', None)
        return estat.get('tipus_competicio', None)
    return None

# Routes principals
@app.route('/')

def index():
    participants = gp.carregar_participants()
    calendari = gpa.generar_calendari_lliga(participants)
    return render_template('index.html',
                         num_participants=len(participants),
                         num_partides=len(calendari))

@app.route('/participants', methods=['GET', 'POST'])
def gestionar_participants():
    error = None
    advertencia = None
    if request.method == 'POST':
        nom = request.form['nom']
        if not gp.validar_nom_participant(nom):
            error = "Nom invàlid! Només lletres i espais permès."
        else:
            resultat = gp.afegir_participant(nom)
            if resultat == "duplicat":
                error = "Participant duplicat! Afegeix una inicial de cognom."
            elif resultat == "ok":
                return redirect(url_for('gestionar_participants'))
    
    participants = gp.carregar_participants()
    
    # Verificar si el número de participants és imparell
    if len(participants) % 2 != 0:
        advertencia = "El número de participants és imparell. Afegeix un altre participant per continuar."

    return render_template('participants.html', 
                         participants=participants,
                         error=error,
                         advertencia=advertencia)

@app.route('/partides', methods=['GET', 'POST'])
def mostrar_partides():
    participants = gp.carregar_participants()
    if not participants or len(participants) < 2:
        error = "Cal almenys 2 participants per generar un torneig."
        return render_template('partides.html', error=error, tipus_competicio=None)

    # Preguntar si se desea cargar un torneig guardado
    if request.method == 'GET' and 'tipus_competicio' not in session:
        if os.path.exists('estat_torneig.json'):
            return render_template('partides.html', 
                                   tipus_competicio=None, 
                                   carregar_pregunta=True)

    if request.method == 'POST':
        if 'carregar_torneig' in request.form and request.form['carregar_torneig'] == 'si':
            tipus_competicio = carregar_estat_torneig()
            if tipus_competicio == "lliga":
                return redirect(url_for('mostrar_partides'))
            elif tipus_competicio == "eliminatories":
                return redirect(url_for('mostrar_partides'))
            else:
                error = "No hi ha cap torneig guardat vàlid."
                return render_template('partides.html', error=error, tipus_competicio=None)

        tipus_competicio = request.form['tipus_competicio']
        session['tipus_competicio'] = tipus_competicio  # Guardar el tipus_competicio en la sesión
        
        if tipus_competicio == "lliga":
            # Preguntar si se desea reiniciar la liga solo en la jornada 1 o si la liga ha finalizado
            if 'calendari_lliga' in session and (
                session.get('jornada_actual', 0) == 0 or session.get('jornada_actual') >= len(session['calendari_lliga'])
            ) and 'reiniciar_lliga' not in request.form:
                return render_template('partides.html', 
                                       tipus_competicio="lliga", 
                                       reiniciar_pregunta=True)

            # Reiniciar la liga si el usuario lo solicita
            if 'reiniciar_lliga' in request.form and request.form['reiniciar_lliga'] == 'si':
                session.pop('calendari_lliga', None)
                session.pop('jornada_actual', None)
                session.pop('puntuacions', None)

            # Inicializar la liga si no está en curso
            if 'jornada_actual' not in session:
                calendari_lliga = gpa.generar_calendari_lliga(participants)
                session['calendari_lliga'] = calendari_lliga
                session['jornada_actual'] = 0
                session['puntuacions'] = gpa.inicialitzar_puntuacions(participants, "lliga")  # Añadir "lliga"

            jornada_actual = session['jornada_actual']
            calendari_lliga = session['calendari_lliga']
            puntuacions = session['puntuacions']

            if jornada_actual < len(calendari_lliga):
                jornada = calendari_lliga[jornada_actual]
                resultats = gpa.simular_partides_jornada(jornada, puntuacions)
                session['jornada_actual'] += 1
                session['puntuacions'] = puntuacions
                return render_template('partides.html', 
                                       resultats=resultats, 
                                       tipus_competicio="lliga", 
                                       jornada_actual=jornada_actual + 1, 
                                       total_jornades=len(calendari_lliga),
                                       guardar_pregunta=True)
            else:
                # Mostrar la pregunta para reiniciar si la liga ha finalizado
                return render_template('partides.html', 
                                       tipus_competicio="lliga", 
                                       reiniciar_pregunta=True)

        elif tipus_competicio == "eliminatories":
            # Verificar si el usuario desea reiniciar la eliminatoria
            if 'reiniciar_eliminatoria' in request.form and request.form['reiniciar_eliminatoria'] == 'si':
                session.pop('calendari_eliminatories', None)
                session.pop('ronda_actual', None)
                session.pop('puntuacions', None)  # Reiniciar puntuaciones
            
                # Inicializar las eliminatorias de nuevo
                calendari_eliminatories = gpa.generar_calendari_eliminatories(participants)
                session['calendari_eliminatories'] = calendari_eliminatories
                session['ronda_actual'] = 0
                session['puntuacions'] = gpa.inicialitzar_puntuacions(participants, "eliminatories")
            
                ronda_actual = session['ronda_actual']
                calendari_eliminatories = session['calendari_eliminatories']
            
                if ronda_actual < len(calendari_eliminatories):
                    ronda = calendari_eliminatories[ronda_actual]
                    resultats = []
                    for partida in ronda:
                        jugador1, jugador2 = partida
                        guanyador = jugador1 if jugador2 == "Bye" else random.choice([jugador1, jugador2])
                        resultats.append((jugador1, jugador2, guanyador))
                    session['ronda_actual'] += 1
                    return render_template('partides.html', 
                                           resultats=resultats, 
                                           tipus_competicio="eliminatories", 
                                           ronda_actual=ronda_actual + 1, 
                                           total_rondes=len(calendari_eliminatories),
                                           guardar_pregunta=True)

            # Verificar si el usuario desea continuar con la siguiente ronda
            if 'cancelar_eliminatoria' in request.form and request.form['cancelar_eliminatoria'] == 'si':
                return render_template('partides.html', 
                                       tipus_competicio="eliminatories", 
                                       eliminatoria_cancelada=True)

            # Obtener o inicializar el estado de las eliminatorias
            if 'calendari_eliminatories' not in session:
                calendari_eliminatories = gpa.generar_calendari_eliminatories(participants)
                session['calendari_eliminatories'] = calendari_eliminatories
                session['ronda_actual'] = 0
                session['puntuacions'] = gpa.inicialitzar_puntuacions(participants, "eliminatories")  # Añadir "eliminatories"

            calendari_eliminatories = session['calendari_eliminatories']
            ronda_actual = session['ronda_actual']

            if ronda_actual < len(calendari_eliminatories):
                ronda = calendari_eliminatories[ronda_actual]
                resultats = []
                for partida in ronda:
                    jugador1, jugador2 = partida
                    guanyador = jugador1 if jugador2 == "Bye" else random.choice([jugador1, jugador2])
                    resultats.append((jugador1, jugador2, guanyador))
                session['ronda_actual'] += 1
                return render_template('partides.html', 
                                       resultats=resultats, 
                                       tipus_competicio="eliminatories", 
                                       ronda_actual=ronda_actual + 1, 
                                       total_rondes=len(calendari_eliminatories))
            else:
                # Si es la última ronda, registrar el ganador
                guanyador = calendari_eliminatories[-1][0][0]  # Primer jugador de la última partida
                session['puntuacions'] = {guanyador: "Guanyador de l'Eliminatòria"}  # Registrar el ganador
                return render_template('partides.html', 
                                       tipus_competicio="eliminatories", 
                                       eliminatoria_finalitzada=True)

        else:
            error = "Tipus de competició no vàlid."
            return render_template('partides.html', error=error, tipus_competicio=None)

    # Si és GET, mostrar el formulari per seleccionar el tipus de competició
    return render_template('partides.html', tipus_competicio=None)

@app.route('/puntuacions')
def mostrar_puntuacions():
    tipus_competicio = session.get('tipus_competicio', None)

    if tipus_competicio == "eliminatories":
            # Mostrar un mensaje de error antes de redirigir al inicio
            flash("Has jugat una eliminatòria. Per veure puntuacions, has de fer una lliga.", "error")
            return redirect(url_for('index'))
    
    elif tipus_competicio == "lliga":
        puntuacions = session.get('puntuacions', {})
        ranquing = punts.generar_ranquing(puntuacions, tipus_competicio)
        return render_template('puntuacions.html', ranquing=ranquing, tipus_competicio="lliga")
    
    else:
        error = "Tipus de competició desconegut."
        return render_template('puntuacions.html', ranquing=[], tipus_competicio=None, error=error)

@app.route('/reset_participants', methods=['POST'])
def reset_participants():
    # Vaciar la lista de participants en el fitxer
    utils.guardar_fitxer('participants.txt', [])  # Guardar una lista vacía en el archivo
    return redirect(url_for('gestionar_participants'))

if __name__ == '__main__':
    app.run(debug=True)