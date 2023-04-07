import os
from  main import app

# Imagens
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