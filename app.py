from flask import Flask, render_template, request, redirect, url_for
import gestio_participants
import gestio_partides
import puntuacions

app = Flask(__name__)

participants = []
partides = []
puntuacions_dict = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/participants', methods=['GET', 'POST'])
def gestionar_participants():
    global participants
    if request.method == 'POST':
        nom = request.form['nom']
        if gestio_participants.afegir_participant(nom):
            participants.append(nom)
        return redirect(url_for('gestionar_participants'))
    return render_template('participants.html', participants=participants)

@app.route('/partides')
def veure_partides():
    return render_template('partides.html', partides=partides)

@app.route('/puntuacions')
def veure_puntuacions():
    ranking = puntuacions.calcular_ranquing(puntuacions_dict)
    return render_template('puntuacions.html', ranking=ranking)

if __name__ == '__main__':
    app.run(debug=True)