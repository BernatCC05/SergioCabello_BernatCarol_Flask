from flask import Flask, render_template, request, redirect, url_for, session
import gestio_participants as gp
import gestio_partides as gpa
import puntuacions as punts
import utils

app = Flask(__name__)
app.secret_key = 'secret_key'

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
    return render_template('participants.html', 
                         participants=participants,
                         error=error)

@app.route('/partides')
def mostrar_partides():
    participants = gp.carregar_participants()
    puntuacions = {participant: 0 for participant in participants}  # Inicializar puntuaciones
    calendari_lliga = gpa.generar_calendari_lliga(participants)
    resultats = gpa.simular_partides(calendari_lliga, puntuacions)
    # Guardar puntuaciones en una variable global o base de datos para usarlas en /puntuacions
    session['puntuacions'] = puntuacions
    return render_template('partides.html', resultats=resultats)

@app.route('/puntuacions')
def mostrar_puntuacions():
    puntuacions = session.get('puntuacions', {})
    ranquing = sorted(puntuacions.items(), key=lambda x: x[1], reverse=True)  # Ordenar por puntos
    return render_template('puntuacions.html', ranquing=ranquing)

@app.route('/reset_participants', methods=['POST'])
def reset_participants():
    # Vaciar la lista de participants
    session['participants'] = []  # Reiniciar la lista de participantes en la sesión
    return redirect(url_for('gestionar_participants'))

if __name__ == '__main__':
    app.run(debug=True)