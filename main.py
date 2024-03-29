from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)

# A URI é formatada por SGBD+DRIVER_CONEXÃO://USUARIO:SENHA@HOST/BANCO_DE_DADOS
app.config.from_pyfile('flask_config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from views_game import *
from views_user import *

# Inicia servidor
if __name__ == "__main__":
    app.run(debug=True)