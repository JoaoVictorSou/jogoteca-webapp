from flask import Flask, render_template
from source.models.jogo import Jogo

# O __name__ faz referência ao próprio módulo.
app = Flask(__name__)

# Rotas

@app.route('/')
def homepage():
    jogo_01 = Jogo("God of War Ragnarok", ["Ação", "Aventura"], ["Playstation 4", "Playstation 5", "PC"])
    jogo_02 = Jogo("Elden Ring", "RPG", ["Playstation 4", "Playstation 5", "Xbox One", "Xbox One X/S", "PC"])
    jogo_03 = Jogo("The Legend of Zelda Breath of The Wild", "RPG", ["Nintendo Switch", "Wii U"])

    print(type(jogo_02.categoria) == list)

    lista_jogos = [
        jogo_01,
        jogo_02,
        jogo_03
    ]

    return render_template("list.html", titulo = 'Jogos', jogos = lista_jogos)

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8080)