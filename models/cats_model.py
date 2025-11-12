from models import db

class Cat(db.Model):
    __tablename__ = "cats"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    adopted = db.Column(db.Boolean, default=False)
    color = db.Column(db.String(50))
    weight = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "breed": self.breed,
            "age": self.age,
            "adopted": self.adopted,
            "color": self.color,
            "weight": self.weight,
        }
