import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

#db_drop_and_create_all()

# ROUTES

@app.route('/drinks',methods=['GET'])

def get_drinks():
    try:
        drinks = Drink.query.all()
    except:
        abort(404)

    
    formatted_drinks = [drink.short() for drink in drinks]

    return jsonify({
        "success" : True,
        "drinks" : formatted_drinks
        })


@app.route('/drinks-detail',methods=['GET'])
@requires_auth(permission='get:drink-details')

def get_drinks_detail(payload):
    print(payload)
    try:
        drinks=Drink.query.all()
    except:
        abort(404)

    formatted_drinks = [drink.long() for drink in drinks]

    return jsonify({
        "success" : True,
        "drinks": formatted_drinks})
      

@app.route('/drinks',methods=['POST'])
@requires_auth(permission='create:drink')

def create_drink(payload):
    body=request.get_json()
    
    new_title=body.get("title")
    new_recipe=body.get("recipe")
    drink=Drink(title=new_title,recipe=json.dumps(new_recipe))


    try:
        drink.insert()
    except Exception as error:
        print(str(error.orig) + " for parameters" + str(error.params))
        abort(422)
    
    return jsonify({
        "success": True,
        "drinks": drink.short()})

@app.route('/drinks/<int:id>',methods=['PATCH'])
@requires_auth(permission='update:drink')

def update_drinks(payload,id):

    try:
        drink=Drink.query.filter(Drink.id==id).one_or_none()

    except Exception as error:
        print(str(error))
        abort(422)
    print(drink)
    if drink is None:
        abort(404)
    else:
        body=request.get_json()

        drink.title = body.get("title")
        drink.recipe = json.dumps(body.get("recipe"))

        try:
            drink.update()

        except Exception as error:
            print(str(error.orig) + "for parameters" + str(error.params))
            abort(422)

    try:
        drinks=Drink.query.filter(Drink.id==id).all()
    except:
        abort(404)

    formatted_drinks = [drink.long() for drink in drinks]

    return jsonify({
        "success" : True,
        "drinks" : formatted_drinks
        })


@app.route('/drinks/<int:id>',methods=['DELETE'])
@requires_auth(permission='delete:drink')

def delete_drink(payload,id):
    try:
        drink=Drink.query.filter(Drink.id==id).one_or_none()
    except Exception as error:
        print(str(error))
        abort(422)

    if drink is None:
        abort(404)
    else:
        try:
            drink.delete()
        except Exception as error:
            print(str(error))
            abort(422)

    return jsonify({
        "success":True,
        "delete":id
        })

# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 422

@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Not Authorized"
    }), 401

@app.errorhandler(403)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden resource"
    }), 403

