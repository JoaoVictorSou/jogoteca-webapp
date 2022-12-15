from flask import Flask, render_template

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)

# Rotas

@app.route('/')
def homepage():
    lista_jogos = [
        "God of War Ragnarok",
        "Elden Ring",
        "The Legend of Zelda Breath of The Wild"
    ]

    return render_template("list.html", titulo = 'Jogos', jogos = lista_jogos)

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8080)