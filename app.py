from flask import Flask, jsonify

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

@app.route('/books')
def get_books():
    return jsonify({'books': books})

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

app.run(port=5000)
