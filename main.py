from flask import Flask, render_template

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)

# Rotas

@app.route('/')
def homepage():
    return render_template("list.html")

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8080)