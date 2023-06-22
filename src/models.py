from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    height=db.Column(db.String(100), nullable=False)
    mass=db.Column(db.String(100), nullable=False)
    birth_year=db.Column(db.String(100), nullable=False)
    eye_color=db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "heigth": self.height,
            "mass": self.mass,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color           
        }

class Planet(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    rotation_period=db.Column(db.String(100), nullable=False)
    orbital_period=db.Column(db.String(100), nullable=False)
    diameter=db.Column(db.String(100), nullable=False)
    climate=db.Column(db.String(100), nullable=False)
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate            
        }
    
class Favorites(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    planet_id=db.Column(db.Integer,db.ForeignKey('planet.id'))
    people_id=db.Column(db.Integer, db.ForeignKey('people.id'))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id') )

    def serialize(self):
        return {
            "id":self.id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
            "user_id": self.user_id
        }
    