import os
from  main import app

def image_recover(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if file_name == f'capa-{id}.jpg':
            return file_name
        else:
            return 'capa-padrao.jpg'