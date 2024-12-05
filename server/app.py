# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add a route to list all Earthquake entries
@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    earthquakes = Earthquake.query.all()
    return jsonify([earthquake.to_dict() for earthquake in earthquakes]), 200

# Add a route to add a new Earthquake entry
@app.route('/earthquakes', methods=['POST'])
def add_earthquake():
    data = request.get_json()
    new_earthquake = Earthquake(
        magnitude=data['magnitude'],
        location=data['location'],
        year=data['year']
    )
    db.session.add(new_earthquake)
    db.session.commit()
    return jsonify(new_earthquake.to_dict()), 201

# Add a route to get a specific Earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    # Query for the earthquake with the given ID
    earthquake = Earthquake.query.get(id)
    
    # If the earthquake is not found, return a 404 with a message
    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    
    # If found, return the earthquake data
    return jsonify(earthquake.to_dict()), 200

# Add a route to get earthquakes by magnitude (greater than or equal to the given magnitude)
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query earthquakes with magnitude >= the given value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Prepare the response data
    earthquake_data = [earthquake.to_dict() for earthquake in earthquakes]
    
    # Return the JSON response with the count and the list of earthquakes
    return jsonify({
        "count": len(earthquake_data),
        "quakes": earthquake_data
    }), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
