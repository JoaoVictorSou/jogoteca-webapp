import os
from  main import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

# Forms
class GameForm(FlaskForm):
    """
    Essa classe deve representar o formulário da aplicação. 
    Ele serve tanto para montar o formulário, 
    como para realizar as validações no servidor.
    """
    name = StringField(
        'Nome do Jogo', 
        [
            validators.DataRequired(), 
            validators.Length(min=1, max=50)
        ]
    )
    category = StringField(
        'Categoria', 
        [
            validators.DataRequired(), 
            validators.Length(min=1, max=40)
        ]
    )
    console = StringField(
        'Console', 
        [
            validators.DataRequired(), 
            validators.Length(min=1, max=20)
        ]
    )
    save = SubmitField('Salvar')

# Image
def image_recover(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa-{id}' in file_name:
            return file_name
        
    return 'capa-padrao.jpg'

def image_delete(id):
    image_name = image_recover(id)

    if image_name != 'capa-padrao.jpg':
        image_path = os.path.join(app.config['UPLOAD_PATH'], image_name)
        os.remove(image_path)

        return True
    else:
        return False