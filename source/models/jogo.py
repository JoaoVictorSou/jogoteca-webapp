class Jogo:
    def __init__(self, nome: str, categoria: list, console: list):
        self.nome = str(nome)
        self.categoria = categoria if type(categoria) == list else [categoria]
        self.console = console if type(console) == list else [console]