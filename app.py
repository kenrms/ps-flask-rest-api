from flask import Flask, jsonify, request, Response
from BookModel import Book
from UserModel import User
from settings import *
import json

import jwt, datetime
from functools import wraps

app.config['SECRET_KEY'] = 'meow'


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token

    return Response('', 401, mimetype='application/json')

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Valid token needed'})
    return wrapper


# GET /books?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})

# GET /books/<isbn>
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

# POST /books
@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if (valid_post_request_data(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    errorMsg = {
        "error": "Invalid book object passed in request",
        "helpString": "Data passed in similar to this {'name': 'bookName', 'price': 8.99, 'isbn': 1234567890}"
    }
    response = Response(json.dumps(errorMsg), status=400, mimetype='application/json')
    return response

# PUT /books/<isbn>
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()

    # Invalid object data in request
    if not valid_put_request_data(request_data):
        errorMsg = {
            'error': 'Valid book object must be passed in the request',
            'helpString': 'Data passed in similar to this {"name": "bookName", "price": 7.99}'
        }
        response = Response(json.dumps(errorMsg), status=400, mimetype='application/json')
        return response

    Book.replace_book(isbn, request_data['name'], request_data['price'])

    response = Response("", status=204)
    return response

# PATCH /books/isbn
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()

    # Do the updates
    if "name" in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if "price" in request_data:
        Book.update_book_price(isbn, request_data['price'])
    
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

# DELETE /books/<isbn>
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", 204)
        return response

    errorMsg = {
        "error": "Book with ISBN " + str(isbn) + " not found."
    }            
    response = Response(json.dumps(errorMsg), 404, mimetype='application/json')
    return response


def valid_post_request_data(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    return False

def valid_put_request_data(bookObject):
    if ("name" in bookObject and "price" in bookObject):
        return True
    return False


app.run(port=5000, debug=True)
