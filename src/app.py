"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def list_users():

    users = User.query.all()
    users = list(map (lambda item: item.serialize(), users ))

    return jsonify(users), 200
    
@app.route('/people', methods=['GET'])
def list_people(): 
    if request.method == 'GET':
        person=People()
        person=person.query.all()
        person=list(map (lambda item: item.serialize(), person ))
        return jsonify(person) ,200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
      if request.method == 'GET':
        persona=People()
        persona = persona.query.get(people_id)
        persona=persona.serialize()
        return jsonify(persona), 200


@app.route('/planets', methods=['GET'])
def planet():
    if request.method == 'GET':
        world=Planet()
        world=world.query.all()
        world=list(map (lambda item: item.serialize(), world ))
        return jsonify(world) ,200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    if request.method == 'GET':
        planet=Planet()
        planet = planet.query.get(planet_id)
        planet=planet.serialize()
        return jsonify(planet), 200

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def list_user_favorites(user_id):
    
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    favorites=list(map (lambda item: item.serialize(), favorites ))
    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>/', methods=['POST'])
def add_planet_favorite(planet_id):
    if request.method =="POST":
        data = request.json

        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify({"message": "Planet not found "}), 404

        existing_favorite = Favorites.query.filter_by(user_id=data["user_id"], planet_id=planet_id).first()
        if existing_favorite:
            return jsonify({"message": "Favorite already exists "}), 404

        new_favorite = Favorites(user_id=data["user_id"], planet_id=planet_id)
        
        db.session.add(new_favorite)
        try:
            db.session.commit()
            return jsonify({"message": "Planet added "}), 200
        except Exception as error:
            return jsonify({"error":error.args}) , 500
        
        
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(people_id):
    if request.method =="POST":
        data = request.json

        people = People.query.get(people_id)
        if people is None:
            return jsonify({"message": "Character not found "}), 404

        existing_favorite = Favorites.query.filter_by(user_id=data["user_id"], people_id=people_id).first()
        if existing_favorite:
            return jsonify({"message": "Favorite already exists "}), 404

        new_favorite = Favorites(user_id=data["user_id"], people_id=people_id)
        db.session.add(new_favorite)
        try:
            db.session.commit()
            return jsonify({"message": "Character added "}), 200
        except Exception as error:
            return jsonify({"error":error.args}) , 500

@app.route('/favorite/planet/<int:planet_id>', methods = ["DELETE"])
def delete_planet(planet_id):
    if request.method == "DELETE":
        data = request.json

        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify({"message": "Planet not found "}), 404

        favorite = Favorites.query.filter_by(user_id=data["user_id"], planet_id=planet_id).first()
        if favorite is None:
            return jsonify({"message": "Favorite not found "}), 404

        db.session.delete(favorite)
        try:
            db.session.commit()
            return jsonify({"message": "Planet removed "}), 200
        except Exception as error:
            return jsonify({"error": error.args}), 500
    



@app.route('/favorite/people/<int:people_id>', methods = ["DELETE"])
def delete_people(people_id):
     if request.method == "DELETE":
        data = request.json

        people = People.query.get(people_id)
        if people is None:
            return jsonify({"message": "People not found "}), 404

        favorite = Favorites.query.filter_by(user_id=data["user_id"], people_id=people_id).first()
        if favorite is None:
            return jsonify({"message": "Favorite not found "}), 404

        db.session.delete(favorite)
        try:
            db.session.commit()
            return jsonify({"message": "People removed "}), 200
        except Exception as error:
            return jsonify({"error": error.args}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
