from main import app
from flask import render_template, redirect, flash, url_for, session, request
from models import User
from helpers import UserForm

@app.route('/login')
def login():
    """
    Rota que disponibiliza página HTML de autenticação.
    """

    form = UserForm()

    next_page = request.args.get('next')

    return render_template(f'login.html', form = form, next_page = next_page)

@app.route('/authenticate', methods = ['POST',])
def authenticate():
    """
    Rota que cria a sessão para acessos com credenciais.
    """
    form = UserForm(request.form)
    next_page = request.form.get('next')

    if form.validate_on_submit():
        match_user = User.query.filter_by(nickname = form.nickname.data).first()
        
        if match_user:
            # The None type converted
            next_page = next_page if next_page != "None" else None 

            if form.password.data == match_user.password:
                session['usuario_logado'] = form.nickname.data
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