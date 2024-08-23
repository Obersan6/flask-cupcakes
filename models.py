"""Models for Cupcake app."""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
# from app import app

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


# Model

class Cupcake(db.Model):
    """Cupcake Model"""

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(300), nullable=False, default='https://tinyurl.com/demo-cupcake')

    # Method to serialize the cupcakes
    def serialize(self):
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }


