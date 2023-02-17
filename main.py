from flask import Flask, render_template, redirect, flash, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
import src.util.security as util_security
import os

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = \
    "{sgbd}://{user}:{security}@{host}/{database}".format(
    sgbd = 'mysql+mysqlconnector',
    user = os.environ.get("MYSQL_TEST_DATABASE_USER"),
    security = os.environ.get("MYSQL_TEST_DATABASE_SECURITY"),
    host = os.environ.get("MYSQL_TEST_DATABASE_HOST"),
    database = 'jogoteca'
)

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    category = db.Column(db.String(40), nullable = False)
    console = db.Column(db.String(20), nullable = False)

    def __repr__(self) -> str:
        return "<Name %r>" % self.name

class User(db.Model):
    nickname = db.Column(db.String(8), primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(200), nullable = False)

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
        match_user = User.query.filter_by(nickname = user_nickname).first()
        
        if match_user:
            # The None type converted
            next_page = next_page if next_page != "None" else None 

            if request.form['senha'] == match_user.password:
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
    if session['usuario_logado']:
        session['usuario_logado'] = None

        flash("Usuário desconectado.")
        return redirect(url_for('login'))
    else:
        flash("Não há conexão para ser desfeita.")
        return redirect(url_for('login'))
    
@app.route('/')
def index():
    """
    Rota para uma página HTML com a lista de todos os jogos da aplicação.
    """
    game_list = Game.query.order_by(Game.id)

    return render_template("list.html", title = 'Jogos', games = game_list)

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
    name = request.form['nome']
    category = request.form['categoria']
    console = request.form['console']


    new_game = Game(
        name = name,
        category = category,
        console = console
    )

    db.session.add(new_game)
    db.session.commit()

    return redirect('/')

# Inicia servidor
if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8080, debug=True)