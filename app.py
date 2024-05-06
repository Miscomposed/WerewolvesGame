from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

players = []
votes = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'player_names' in request.form:
            player_names = request.form['player_names']
            names = [name.strip() for name in player_names.replace(',', '\n').split('\n') if name.strip()]
            for name in names:
                players.append({'name': name, 'status': 'Alive', 'role': 'Villager'})
        elif 'start_game' in request.form:
            # Add game starting logic here if needed
            pass
        elif 'reset_game' in request.form:
            players.clear()
            votes.clear()
        elif 'next_round' in request.form:
            votes.clear()  # Reset the votes for the next round
        return redirect(url_for('home'))
    return render_template('home.html', players=players)


@app.route('/update', methods=['POST'])
def update():
    player_name = request.form['player_name']
    role = request.form['role']
    status = request.form['status']
    for player in players:
        if player['name'] == player_name:
            player['role'] = role
            player['status'] = status
            if status == 'Dead':
                votes.pop(player_name, None)  # Remove the player's vote if they are dead
            break
    return redirect(url_for('home'))


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        voter = request.form['voter']
        candidate = request.form['candidate']
        votes[voter] = candidate
        return redirect(url_for('vote'))
    alive_players = [player for player in players if player['status'] == 'Alive']
    return render_template('vote.html', players=alive_players, votes=votes)


if __name__ == '__main__':
    app.debug = True
    app.run()
