from . import db
from sqlalchemy.sql import func
    
class Signatures(db.Model):
    __tablename__ = "Signatures"
    id = db.Column(db.Integer, primary_key=True)
    classe = db.Column(db.String(100))
    condition = db.Column(db.String(1000), nullable=False)
    data = db.Column(db.String(1000), nullable=False)
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