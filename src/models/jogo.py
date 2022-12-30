class Jogo:
    def __init__(self, nome: str, categoria: list, console: list):
        self.nome = str(nome)
        self.categoria = categoria if type(categoria) == list else [categoria]
        self.console = console if type(console) == list else [console]

jogo_01 = Jogo("God of War Ragnarok", ["Ação", "Aventura"], ["Playstation 4", "Playstation 5", "PC"])
jogo_02 = Jogo("Elden Ring", "RPG", ["Playstation 4", "Playstation 5", "Xbox One", "Xbox One X/S", "PC"])
jogo_03 = Jogo("The Legend of Zelda Breath of The Wild", "RPG", ["Nintendo Switch", "Wii U"])

lista_jogos = [
    jogo_01,
    jogo_02,
    jogo_03
]