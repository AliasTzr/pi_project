from . import db, socketio
from sqlalchemy.sql import func
from sqlalchemy import event
    
# 🔹 Modèle Utilisateur
class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # 
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class Signatures(db.Model):
    __tablename__ = "Signatures"
    id = db.Column(db.Integer, primary_key=True)
    classe = db.Column(db.String(100))
    condition = db.Column(db.String(1000), nullable=False)
    data = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 🔹 Clé étrangère vers User
    user = db.relationship('User', backref=db.backref('signatures', lazy=True))  # Relation
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def serialyse(self):
        return {
            "id": self.id,
            "classe": self.classe,
            "data": self.data,
            "condition": self.condition,
            "created_at": self.created_at
        }
# 🔹 Écoute les insertions dans Signatures et envoie une notification en temps réel
def after_insert_listener(mapper, connection, target):
    # 🔹 Récupérer toutes les signatures de l'utilisateur
    user_signatures = Signatures.query.filter_by(user_id=target.user_id).all()

    # 🔹 Convertir en liste de dictionnaires
    signatures_list = [
        {
            "id": sig.id,
            "classe": sig.classe,
            "condition": sig.conditon,
            "data": sig.data
        }
        for sig in user_signatures
    ]

    # 🔹 Envoyer la liste complète au client WebSocket de l'utilisateur concerné
    socketio.emit(f"new_entry_{target.user_id}", signatures_list)

# 🔹 Associer l'événement `after_insert` au modèle Signatures
event.listen(Signatures, "after_insert", after_insert_listener)