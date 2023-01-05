from flask import Flask, render_template, redirect, flash, url_for, session, request
from src.models.jogo import Jogo, lista_jogos
from src.models.user import User, user_list
from src.database.database_generator import Database
import src.util.security as util_security

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)
app.secret_key = 'Nintendo'

# Rotas
@app.route('/test_features') # Não vai para "produção"
def test_features():
    """
        Essa rota server para pequenos testes de funcionamento de features
    """
    database = Database('localhost', 'root')
    print("Database conection: " + database.to_connect(util_security.get_mysql_security())['message'])
    
    print(f"print: {database._check_tables_exists('mysql', ['role_edges', 'columns_priv'])}")

    return 't'

@app.route('/login')
def login():
    """
    Rota que disponibiliza página HTML de autenticação.
    """
    next_page = request.args.get('next')

    return render_template(f'login.html', next_page = next_page)

@app.route('/authenticate', methods = ['POST',])
def authenticate():
    """
    Rota que cria a sessão para acessos com credenciais.
    """
    user_nickname = request.form.get('usuario')
    next_page = request.form.get('next')

    if user_nickname:
        matched_user = None

        for user in user_list:
            if user.nickname == user_nickname:
                matched_user = user
        
        if matched_user:
            # The None type converted
            next_page = next_page if next_page != "None" else None 

            if request.form['senha'] == matched_user.password:
                session['usuario_logado'] = request.form['usuario']
                flash('Usuário logado com sucesso!')
                
                print(type(next_page))

                if next_page:
                    return redirect(next_page)
                
                return redirect(url_for('index'))
    
    flash('Usuário não logado.')
    return redirect(url_for('login', next = next_page))

@app.route('/logout')
def logout():
    """
    Rota para finalizar a sessão no servidor.
    """
    session['usuario_logado'] = None

    flash("Usuário desconectado.")

    return redirect(url_for('login'))

@app.route('/')
def index():
    """
    Rota para uma página HTML com a lista de todos os jogos da aplicação.
    """
    return render_template("list.html", titulo = 'Jogos', jogos = lista_jogos)

@app.route('/game/register', methods = ["GET",])
def show_register_game_page():
    """
    Rota que disponibiliza formulário HTML para acrescentar jogos na aplicação.
    """
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash("Faça login antes de adicionar jogos.")
        
        return redirect(url_for('login', next='game/register'))
    
    return render_template('new_game.html', titulo = 'Novo Jogo')

@app.route('/game/create', methods = ["POST",])
def create_game():
    """
    Rota que salva os jogos cadastrados para que possam ser acessados nos termos da aplicação.
    """
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