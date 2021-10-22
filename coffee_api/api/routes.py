from os import name
from flask import Blueprint, request, jsonify
from coffee_api.models import Flight, db, flight_schema, flights_schema
from coffee_api.helpers import token_required

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 'Coding Temple'}

@api.route('/flights', methods=['POST'])
@token_required
def create_flight(current_user_token):
    departsin_landsin = request.json['departsin_landsin']
    flight_duration = request.json['flight_time']
    max_speed = request.json['max_speed']
    cost_of_flight = request.json['cost_of_flight']
    plane_series = request.json['plane_series']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    flight = Flight(departsin_landsin,flight_duration,max_speed,cost_of_flight,plane_series, user_token = token)

    db.session.add(flight)
    db.session.commit()

    response = flight_schema.dump(flight)
    return jsonify(response)

@api.route('/flights', methods = ['GET'])
@token_required
def get_flights(current_user_token):
    owner = current_user_token.token
    flights = Flight.query.filter_by(user_token = owner).all()
    response = flights_schema.dump(flights)
    return jsonify(response)

@api.route('/flights/<id>', methods = ['GET'])
@token_required
def get_flight(current_user_token, id):
    flight = Flight.query.get(id)
    if flight:
        print(f'Here is your Flight: {flight.name}')
        response = flight_schema.dump(flight)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That Flight does not exist!'})


@api.route('/flights/<id>', methods = ['POST', 'PUT'])
@token_required
def update_flight(current_user_token, id):
    flight = Flight.query.get(id)
    print(flight)
    if flight:
        flight.name = request.json['name']
        flight.description = request.json['description']
        flight.camera_quality = request.json['camera_quality']
        flight.flight_time = request.json['flight_time']
        flight.max_speed = request.json['max_speed']
        flight.dimensions = request.json['dimensions']
        flight.weight = request.json['weight']
        flight.cost_of_prod = request.json['cost_of_prod']
        flight.series = request.json['series']
        flight.user_token = current_user_token.token
        db.session.commit()

        response = flight_schema.dump(flight)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That flight does not exist!'})

@api.route('/flights/<id>', methods = ['DELETE'])
@token_required
def delete_flight(current_user_token, id):
    flight = Flight.query.get(id)
    if flight:
        db.session.delete(flight)
        db.session.commit()
        return jsonify({'Success': f'Flight ID #{flight.id} has been deleted'})
    else:
        return jsonify({'Error': 'That flight does not exist!'})




