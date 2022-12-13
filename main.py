from flask import Flask

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)

# Rotas

@app.route('/')
def homepage():
    return {"data": "Hello, world"}

if __name__ == "__main__":
    app.run()