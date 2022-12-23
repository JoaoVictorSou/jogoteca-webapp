from flask import Flask, render_template, redirect, flash, url_for, session, request
from source.models.jogo import Jogo, lista_jogos

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)
app.secret_key = 'Nintendo'
# Rotas
@app.route('/login')
def login():
    next_page = request.args.get('next')

    return render_template(f'login.html', next_page = next_page)

@app.route('/authenticate', methods = ['POST',])
def authenticate():
    # The None type converted
    next_page = request.form.get('next')
    next_page = next_page if next_page != "None" else None 

    if request.form['senha'] == 'alohomora':
        session['usuario_logado'] = request.form['usuario']
        flash('Usuário logado com sucesso!')
        
        print(type(next_page))

        if next_page:
            return redirect(f'/{next_page}')
        
        return redirect(url_for('index'))
    
    flash('Usuário não logado.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None

    flash("Usuário desconectado.")

    return redirect(url_for('login'))


@app.route('/')
def index():
    
    return render_template("list.html", titulo = 'Jogos', jogos = lista_jogos)

@app.route('/game/register', methods = ["GET",])
def show_register_game_page():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash("Faça login antes de adicionar jogos.")
        
        return redirect(url_for('login', next='game/register'))
    
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

# Inicia servidor
if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8080, debug=True)