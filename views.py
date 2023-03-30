from flask import render_template, redirect, flash, url_for, session, request
from models import Game, User
from main import app, db

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

@app.route('/game/register', methods = ["POST",])
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
    if session.get('usuario_logado'):
        session['usuario_logado'] = None

        flash("Usuário desconectado.")
        return redirect(url_for('login'))
    else:
        flash("Não há conexão para ser desfeita.")
        return redirect(url_for('login'))
