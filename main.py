from flask import Flask, render_template, redirect, flash, session, request
from source.models.jogo import Jogo, lista_jogos

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)
app.secret_key = 'Nintendo'
# Rotas
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods = ['POST',])
def authenticate():
    if request.form['senha'] == 'alohomora':
        session['usuario_logado'] = request.form['usuario']
        flash('Usuário logado com sucesso!')
        
        return redirect('/')
    
    flash('Usuário não logado.')
    return redirect('/login')

@app.route('/')
def index():
    
    return render_template("list.html", titulo = 'Jogos', jogos = lista_jogos)

@app.route('/game/register', methods = ["GET",])
def show_register_game_page():
    return render_template('new_game.html', titulo = 'Novo Jogo')

@app.route('/game/create', methods = ["POST",])
def create_game():
    print(request)
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    lista_jogos.append(
        Jogo(nome, categoria, console)
    )

    return redirect('/')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None

    flash("Usuário desconectado.")

    return redirect('/login')

# Inicia servidor
if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8080, debug=True)