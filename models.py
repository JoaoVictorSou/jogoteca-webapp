from main import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)
    category = db.Column(db.String(40), nullable = False)
    console = db.Column(db.String(20), nullable = False)

    def __repr__(self) -> str:
        return "<Name %r>" % self.name

class User(db.Model):
    nickname = db.Column(db.String(8), primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(200), nullable = False)