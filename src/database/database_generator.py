import mysql.connector
from mysql.connector import errorcode

class Database():
      def __init__(self, host, user):
            self._host = host
            self._user = user
      
      @property
      def conn(self):
            return self.__conn

      def to_connect(self, password):
            try:
                  self.__conn = mysql.connector.connect(
                        host= self._host,
                        user= self._user,
                        password= password
                  )
            except mysql.connector.ProgrammingError as err:
                  if err.errno == 1045:
                        return {'message': err.msg, 'errno': err.errno}
                  else:
                        return {'message': f'MySQLConnectorProgrammingError: {err.errno}', 'code': '500'}

            except mysql.connector.Error as err:
                  return {'messege': err.msg, 'errno': err.errno}
            
            return {'messege': 'Database connection worked', 'errno': None}

      def start_base(self):
            cursor = self.__conn.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS `jogoteca`;")

            cursor.execute("USE `jogoteca`;")

            # criando tabelas
            TABLES = {}
            TABLES['Jogos'] = ('''
                  CREATE TABLE `jogos` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `nome` varchar(50) NOT NULL,
                  `categoria` varchar(40) NOT NULL,
                  `console` varchar(20) NOT NULL,
                  PRIMARY KEY (`id`)
                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

            TABLES['Usuarios'] = ('''
                  CREATE TABLE `usuarios` (
                  `nome` varchar(20) NOT NULL,
                  `nickname` varchar(8) NOT NULL,
                  `senha` varchar(100) NOT NULL,
                  PRIMARY KEY (`nickname`)
                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

            for tabela_nome in TABLES:
                  tabela_sql = TABLES[tabela_nome]
                  try:
                        print('Criando tabela {}:'.format(tabela_nome), end=' ')
                        cursor.execute(tabela_sql)
                  except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                              print('Já existe')
                        else:
                              print(err.msg)
                  else:
                        print('OK')

            # inserindo usuarios
            usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
            usuarios = [
                  ("Bruno Divino", "BD", "alohomora"),
                  ("Camila Ferreira", "Mila", "paozinho"),
                  ("Guilherme Louro", "Cake", "python_eh_vida")
            ]
            cursor.executemany(usuario_sql, usuarios)

            cursor.execute('select * from jogoteca.usuarios')
            print(' -------------  Usuários:  -------------')
            
            for user in cursor.fetchall():
                  print(user[1])

            # inserindo jogos
            jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
            jogos = [
                  ('Tetris', 'Puzzle', 'Atari'),
                  ('God of War', 'Hack n Slash', 'PS2'),
                  ('Mortal Kombat', 'Luta', 'PS2'),
                  ('Valorant', 'FPS', 'PC'),
                  ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
                  ('Need for Speed', 'Corrida', 'PS2'),
            ]
            cursor.executemany(jogos_sql, jogos)

            cursor.execute('select * from jogoteca.jogos')
            print(' -------------  Jogos:  -------------')
            for jogo in cursor.fetchall():
                  print(jogo[1])

            # commitando se não nada tem efeito
            self.__conn.commit()

            cursor.close()
      
      def database_exists(self, database_name):
            query_database_exists = "SHOW DATABASES LIKE %s"

            cursor = self.__conn.cursor()
            
            cursor.execute(query_database_exists, [database_name,])
            
            exists = True if cursor.fetchone() is not None else False
            
            cursor.close()

            return exists
      
"""
conn.close()
"""