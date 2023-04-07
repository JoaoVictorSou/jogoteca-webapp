from flask import render_template, redirect, flash, url_for, session, request, send_from_directory
from models import Game, User
from helpers import image_recover, image_delete, GameForm
from main import app, db
import time

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
    
    form = GameForm()

    return render_template('new_game.html', titulo = 'Novo Jogo', form = form)
    

@app.route('/game/register', methods = ["POST",])
def create_game():
    """
    Rota que salva os jogos cadastrados para que possam ser acessados nos termos da aplicação.
    """
    if session.get('usuario_logado'):
        form = GameForm(request.form) # Basta que o formulário seja utilizado na instância do JWT e não precisará mais acessar o request
        if form.validate_on_submit():
            name = form.name.data
            category = form.category.data
            console = form.console.data
            game_image = request.files.get('game_image')
            upload_path = app.config['UPLOAD_PATH']
            timestamp = time.time()

            new_game = Game(
                name = name,
                category = category,
                console = console
            )

            db.session.add(new_game)
            db.session.commit()

            if game_image:
                game_image.save(f'{upload_path}/capa-{new_game.id}-{timestamp}.jpg')

            flash('Jogo registrado!')
            return redirect('/')
        
        else:
            flash('Preencha todos os campos obrigatórios!')
            return redirect(url_for('show_register_game_page'))
    
    flash("É necessário estar logado para registrar um jogo!")
    return redirect(url_for('index'))

@app.route('/game/edit/<int:id>', methods=("GET",))
def edit_game_page(id):
    if session.get('usuario_logado'):
        game = Game.query.get(id)
        
        if game:
            game_image = image_recover(game.id)
            form = GameForm()

            form.name.data = game.name
            form.category.data = game.category
            form.console.data = game.console
            
            return render_template(
                'edit-game.html',
                id = id,
                game_image = game_image,
                form = form
            )
        else:
            flash('Você só pode editar um jogo que esteja cadastrado.')
            return redirect(url_for('index'))
    else:
        flash('Você precisa estar logado primeiro!')
        return redirect(url_for('login', next = f'game/edit/{id}'))

@app.route('/game/edit', methods=('POST',))
def edit_game_process():
    if session.get('usuario_logado'):
        id = request.form.get('id')
        game = Game.query.get(id)

        if game:
            form = GameForm(request.form)
            if form.validate_on_submit():
                game.name = form.name.data
                game.category = form.category.data
                game.console = form.console.data
                game_image = request.files.get('game_image')
                timestamp = time.time()
                upload_path = app.config['UPLOAD_PATH']

                if game_image:
                    image_delete(game.id)
                    game_image.save(f"{upload_path}/capa-{game.id}-{timestamp}.jpg")

                db.session.add(game)
                db.session.commit()

                flash('Jogo alterado!')
                return redirect(url_for('index'))
            else:
                flash("Preencha os campos obrigatórios!")
                return redirect(url_for('edit_game_page', id = id))
        else:
            flash('Não existe jogo correspondente ao ID informado.')
            return redirect(url_for('index'))
    else:
        flash("É necessário estar logado para a alteração de dados.")
        return redirect(url_for('index'))

@app.route('/game/remove/<int:id>', methods=('GET',))
def game_remove_process(id):
    if session.get('usuario_logado'):
        game = Game.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Jogo deletado com sucesso!')
        return redirect(url_for('index'))
    
    flash('Apenas usuários logados podem deletar registros!')
    return redirect(url_for('login'))

@app.route('/game/static/<filename>')
def game_static(filename):
    file_type = request.args.get('file_type')
    
    if file_type == 'image':
        return send_from_directory('uploads', filename)

    return redirect(url_for('index'), code=400)

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
                
                print(next_page)
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
