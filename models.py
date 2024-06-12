from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Enquete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    opcoes = db.relationship('Opcao', backref='enquete', cascade="all, delete-orphan", lazy=True)

class Opcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    votos = db.Column(db.Integer, default=0)
    enquete_id = db.Column(db.Integer, db.ForeignKey('enquete.id'), nullable=False)
