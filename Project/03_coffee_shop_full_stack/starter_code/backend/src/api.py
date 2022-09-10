import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
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

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation#n$env
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail',methods=['GET'])
def get_drinks_detail():
    try:
        drinks=Drink.query.all()
    except:
        abort(404)

    formatted_drinks = [drink.long() for drink in drinks]

    return jsonify({
        "success" : True,
        "drinks": formatted_drinks})
      

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks',methods=['POST'])
def create_drink():
    body=request.get_json()
    
    new_title=body.get("title")
    new_recipe=body.get("recipe")
    print(json.dumps(new_recipe))
    drink=Drink(title=new_title,recipe=json.dumps(new_recipe))
    print(new_title)
    print(new_recipe)

    try:
        drink.insert()
    except Exception as error:
        print(str(error.orig) + " for parameters" + str(error.params))
        abort(422)
    
    return jsonify({
        "success": True,
        "drinks": drink.short()})

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>',methods=['PATCH'])
def update_drinks(id):

    try:
        drink=Drink.query.filter(Drink.id==id).one_or_none()

    except Exception as error:
        print(str(error))
        abort(422)

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

    return jsonify({
        "success" : True,
        "drinks" : drink.long()
        })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>',methods=['DELETE'])
def delete_drink(id):
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
'''
Example error handling for unprocessable entity
'''


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

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
