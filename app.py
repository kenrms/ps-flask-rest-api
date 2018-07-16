from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 234234234
    },
    {
        'name': 'The Cat In the Hat',
        'price': 6.99,
        'isbn': 123123123
    }
]


def valid_post_request_data(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    return False

def valid_put_request_data(bookObject):
    if ("name" in bookObject and "price" in bookObject):
        return True
    return False


# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})

# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (valid_post_request_data(request_data)):
        new_book = {
            "name": request_data['name'],
            "price":request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    errorMsg = {
        "error": "Invalid book object passed in request",
        "helpString": "Data passed in similar to this {'name': 'bookName', 'price': 8.99, 'isbn': 1234567890}"
    }
    response = Response(json.dumps(errorMsg), status=400, mimetype='application/json')
    return response

# GET /books/<isbn>
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

# PUT /books/<isbn>
@app.route('/books/<int:isbn>', methods=['PUT'])
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

    # New book data
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }

    # Find and replace book data
    for i in range(0, len(books)):
        book = books[i]
        currentIsbn = book['isbn']
        if currentIsbn == isbn:
            books[i] = new_book
            break

    response = Response("", status=204)
    return response

# PATCH /books/isbn
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}

    # What are we updating?
    if "name" in request_data:
        updated_book['name'] = request_data['name']
    if "price" in request_data:
        updated_book['price'] = request_data['price']

    # Okay, find the book and update it
    for i in range(0, len(books)):
        book = books[i]
        if book['isbn'] == isbn:
            book.update(updated_book)
            break
    
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

# DELETE /books/<isbn>
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    for i in range(0, len(books)):
        book = books[i]
        if book['isbn'] == isbn:
            del books[i]
            response = Response("", 204)
            return response

    errorMsg = {
        "error": "Book with ISBN " + str(isbn) + " not found."
    }            
    response = Response(json.dumps(errorMsg), 404, mimetype='application/json')
    return response


app.run(port=5000, debug=True)
