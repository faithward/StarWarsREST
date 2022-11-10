from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    birth_year = db.Column(db.String(10), unique=False, nullable=False)
    homeworld = db.Column(db.String(50), unique=False, nullable=False)
    FavChar = db.relationship('FavChar', lazy=True)
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "birth_year" : self.birth_year,
            "homeworld" : self.homeworld
        }
class FavChar(db.Model):
    __tablename__ = 'favPerson'
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    
    def serialize(self):
        return {
            "id" : self.id,
            "people_id" : self.people_id
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.String(15), nullable=False)
    population = db.Column(db.String(18), nullable=False)
    FavPlanet = db.relationship('FavPlanet', lazy=True)
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "diameter" : self.diameter,
            "population" : self.population
        }
class FavPlanet(db.Model):
    __tablename__ = 'favPlanet'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    def serialize(self):
        return {
            "id" : self.id,
            "planet_id" : self.planet_id
        }


