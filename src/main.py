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
from models import db, User, People, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/user', methods=['GET'])
def getUsers():

    userQuery = User.query.all()
    allUsers = list(map(lambda x: x.serialize(), userQuery))

    return jsonify(allUsers), 200

@app.route('/user', methods=['POST'])
def createUser():
    body = request.get_json()
    if body == None:
        return "The request body is null", 400
    if 'email' not in body:
        return "Add the user email", 400
    if 'password' not in body:
        return "Add user password", 400
    if 'is_active' not in body:
        return "Add user activity status", 400
    print(body)
    newUser = User(email=body["email"], password=body["password"], is_active=body["is_active"])
    db.session.add(newUser)
    db.session.commit()

    return 'User has been created', 200

@app.route('/user/<int:id>', methods=['PUT'])

def updateUser(id):
    user1 = User.query.get(id)
    body = request.get_json()
    if body == None:
        return 'Body is empty', 400
    if 'email' not in body:
        return 'Add the user email', 400
    user1.email = body["email"]
    db.session.commit()

    return 'ok'

@app.route('/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
    user1 = User.query.get(id)
    if user1 == None:
        raise APIException('User does not exist', status_code=404)
    
    db.session.delete(user1)
    db.session.commit()
    return 'User deleted'

@app.route('/people', methods=['GET'])
def getPeople():
    personQuery = People.query.all()
    allPeople = list(map(lambda x: x.serialize(), personQuery))

    return jsonify(allPeople), 200

@app.route('/people', methods=['POST'])
def createPerson():
    body = request.get_json()
    if body == None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add the person's name", 400
    if 'birth_year' not in body:
        return "Add person's birthyear", 400
    if 'homeworld' not in body:
        return "Add person's homeworld", 400
    print(body)
    newPerson = People(name=body["name"], birth_year=body["birth_year"], homeworld=body["homeworld"])
    db.session.add(newPerson)
    db.session.commit()

    return 'Person has been created', 200

@app.route('/people/<int:id>', methods=['PUT'])
def updatePerson(id):
    char1 = People.query.get(id)
    body = request.get_json()
    if body == None:
        return 'Body is empty', 400
    if 'name' in body:
        return 'Name cannot be edited', 400
    if 'birth_year' in body:
        char1.birth_year = body["birth_year"]
    elif 'homeworld' in body:
        char1.homeworld = body["homeworld"]
    
    db.session.commit()

    return "Person's data has been updated", 200

@app.route('/people/<int:id>', methods=['GET'])
def getPerson(id):
    personQuery = People.query.get(id)
    if personQuery == None:
        raise APIException('Person does not exist', status_code=404)
    data = personQuery.serialize()

    return jsonify(data), 200

@app.route('/people/<int:id>', methods=['DELETE'])
def deletePerson(id):
    char1 = People.query.get(id)
    if char1 == None:
        raise APIException('Person does not exist', status_code=404)
    db.session.delete(char1)
    db.session.commit()
    return 'Person deleted'

@app.route('/planet', methods=['POST'])
def createPlanet():
    body = request.get_json()
    if body == None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add the planet's name", 400
    if 'diameter' not in body:
        return "Add the planet's diameter", 400
    if 'population' not in body:
        return "Add the planet's population", 400
    newPlanet = Planet(name=body["name"], diameter=body["diameter"], population=body["population"])
    db.session.add(newPlanet)
    db.session.commit()

    return 'Planet has been created', 200

@app.route('/planet', methods=['GET'])
def getPlanets():
    planetQuery = Planet.query.all()
    allPlanets = list(map(lambda x: x.serialize(), planetQuery))

    return jsonify(allPlanets), 200

@app.route('/planet/<int:id>', methods=['GET'])
def getPlanet(id):
    planetQuery = Planet.query.get(id)
    if planetQuery == None:
        raise APIException('Planet does not exist', status_code=404)
    data = planetQuery.serialize()

    return jsonify(data), 200


@app.route('/planet/<int:id>', methods=['PUT'])
def updatePlanet(id):
    plan = Planet.query.get(id)
    body = request.get_json()
    if body == None:
        return 'Body is empty', 400
    if 'name' in body:
        return 'Name cannot be edited', 400
    if 'diameter' in body:
        plan.diameter = body["diameter"]
    elif 'homeworld' in body:
        plan.population = body["population"]
    
    db.session.commit()

    return 'Planet data has been updated', 200

@app.route('/planet/<int:id>', methods=['DELETE'])
def deletePlanet(id):
    plan = Planet.query.get(id)
    if plan == None:
        raise APIException('Planet does not exist', status_code=404)
    db.session.delete(plan)
    db.session.commit()
    return 'Planet deleted'

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
