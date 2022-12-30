class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password

user_01 = User("João Victor", "sljoaos", "pypi")
user_02 = User("Rafael Fernandes", "vovorafa", "vfvf")
user_03 = User("Pedro Afonso", "predu", "sadsad")

user_list = [user_01, user_02, user_03]