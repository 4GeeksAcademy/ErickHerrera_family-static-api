"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_family_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as error:
        return jsonify({"msg": str(error)}), 500


@app.route('/member', methods=['POST'])
def add_family_member():
    member = request.get_json()
    if not member:
        return jsonify({"msg": "Datos invalidos"}), 400
    try:
        new_member = jackson_family.add_member(member)
        return jsonify(new_member), 200 
    except Exception as error:
        return jsonify({"msg": str(error)}), 500
    

@app.route('/member/<int:id>', methods=['GET'])
def get_family_member(id):
    try:
        member = jackson_family.get_member(id) 
        if member:
            return jsonify(member), 200  
        else:
            return jsonify({"msg": "Miembro no encontrado"}), 404
    except Exception as error:
        return jsonify({"msg": str(error)}), 500
    

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_family_member(id):
    try:
        removed_member = jackson_family.delete_member(id)
        if removed_member:
            return jsonify({"done": True}), 200  
        else:
            return jsonify({"done": False}), 404
    except Exception as error:
        return jsonify({"msg": str(error)}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
