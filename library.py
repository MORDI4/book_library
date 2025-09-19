from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from app.models import db, Books, Authors, Rentals
from app import create_app


app = create_app()

# ------------------------------
# Strona webowa
# ------------------------------

@app.route('/')
def main_page():
    books = Books.query.all()
    rentals = Rentals.query.all()
    return render_template("homepage.html", books=books, rentals=rentals)

@app.route('/status_update/<int:book_id>')
def status_update(book_id):
    rental = Rentals.query.filter_by(book_id=book_id).first()
    if rental == None:
        new_rental = Rentals(book_id=book_id, rental_date=date.today(), returned=False)
        db.session.add(new_rental)
    elif rental.returned == False:
        rental.returned = True
        rental.return_date = date.today()
    elif rental.returned == True:
        new_rental = Rentals(book_id=book_id, rental_date=date.today(), returned=False)
        db.session.add(new_rental)
    db.session.commit()
    return redirect(url_for("main_page"))

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = Books.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        # obsługa autorów, np. split(',') i przypisanie listy Author
        book.year_published = request.form.get('year_published')
        book.genre = request.form.get('genre')
        book.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('main_page'))
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:book_id>')
def delete(book_id):
    book = Books.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("main_page"))

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    a_name = request.form['author'].split()[0]
    a_surname = request.form['author'].split()[1]
    author = Authors.query.filter_by(
            name=a_name, 
            surname=a_surname
        ).first()
    year = request.form.get('year_published')
    genre = request.form.get('genre')
    description = request.form.get('description')
    
    if author == None:
        author1 = Authors(name=a_name, surname=a_surname)
        db.session.add(author1)
        db.session.commit()
        author = Authors.query.filter_by(
            name=a_name, 
            surname=a_surname
        ).first()
    
    book1 = Books(
        title=title,
        description=description,
        genre=genre,
        year_published=year,
        authors= [author]
    )
    db.session.add(book1)
    db.session.commit()
    return redirect(url_for('main_page'))

# ------------------------------
# REST API endpoints for Books
# ------------------------------
@app.route('/api/books', methods=['GET'])
def api_get_books():
    books = Books.query.all()
    data = []
    for book in books:
        data.append({
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'genre': book.genre,
            'year_published': book.year_published,
            'authors': [f"{a.name} {a.surname}" for a in book.authors]
        })
    return jsonify(data)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
    book = Books.query.get_or_404(book_id)
    data = {
        'id': book.id,
        'title': book.title,
        'description': book.description,
        'genre': book.genre,
        'year_published': book.year_published,
        'authors': [f"{a.name} {a.surname}" for a in book.authors]
    }
    return jsonify(data)

@app.route('/api/books', methods=['POST'])
def api_add_book():
    data = request.json
    title = data.get('title')
    author_fullname = data.get('author')  # np. "Jan Kowalski"
    year = data.get('year_published')
    genre = data.get('genre')
    description = data.get('description')

    a_name, a_surname = author_fullname.split()
    author = Authors.query.filter_by(name=a_name, surname=a_surname).first()
    if author is None:
        author = Authors(name=a_name, surname=a_surname)
        db.session.add(author)
        db.session.commit()

    book1 = Books(
        title=title,
        description=description,
        genre=genre,
        year_published=year,
        authors=[author]
    )
    db.session.add(book1)
    db.session.commit()
    return jsonify({'message': 'Book added', 'book_id': book1.id}), 201

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def api_delete_book(book_id):
    book = Books.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def api_update_book(book_id):
    book = Books.query.get_or_404(book_id)
    data = request.json

    # Aktualizacja pól książki
    if 'title' in data:
        book.title = data['title']
    if 'description' in data:
        book.description = data['description']
    if 'genre' in data:
        book.genre = data['genre']
    if 'year_published' in data:
        book.year_published = data['year_published']

    # Aktualizacja autora
    if 'author' in data:
        a_name, a_surname = data['author'].split()
        author = Authors.query.filter_by(name=a_name, surname=a_surname).first()
        if author is None:
            author = Authors(name=a_name, surname=a_surname)
            db.session.add(author)
            db.session.commit()
        book.authors = [author]

    db.session.commit()

    return jsonify({
        'message': 'Book updated',
        'book': {
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'genre': book.genre,
            'year_published': book.year_published,
            'authors': [f"{a.name} {a.surname}" for a in book.authors]
        }
    })


# ------------------------------
# REST API endpoints for Authors
# ------------------------------
@app.route('/api/authors', methods=['GET'])
def api_get_authors():
    authors = Authors.query.all()
    data = []
    for author in authors:
        data.append({
            'id': author.id,
            'name': author.name,
            'surname': author.surname,
            'books': [book.title for book in author.books]
        })
    return jsonify(data)

@app.route('/api/authors/<int:author_id>', methods=['GET'])
def api_get_author(author_id):
    author = Authors.query.get_or_404(author_id)
    data = {
        'id': author.id,
        'name': author.name,
        'surname': author.surname,
        'books': [book.title for book in author.books]
    }
    return jsonify(data)

@app.route('/api/authors', methods=['POST'])
def api_add_author():
    data = request.json
    name = data.get('name')
    surname = data.get('surname')

    author = Authors.query.filter_by(name=name, surname=surname).first()
    if author is None:
        author = Authors(name=name, surname=surname)
        db.session.add(author)
        db.session.commit()

    return jsonify({'message': 'Author added', 'author_id': author.id}), 201

@app.route('/api/authors/<int:author_id>', methods=['PUT'])
def api_update_author(author_id):
    author = Authors.query.get_or_404(author_id)
    data = request.json
    if 'name' in data:
        author.name = data['name']
    if 'surname' in data:
        author.surname = data['surname']
    db.session.commit()
    return jsonify({
        'message': 'Author updated',
        'author': {
            'id': author.id,
            'name': author.name,
            'surname': author.surname
        }
    })

@app.route('/api/authors/<int:author_id>', methods=['DELETE'])
def api_delete_author(author_id):
    author = Authors.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({'message': 'Author deleted'})

# ------------------------------
# REST API endpoints for Rentals
# ------------------------------
@app.route('/api/rentals', methods=['GET'])
def api_get_rentals():
    rentals = Rentals.query.all()
    data = []
    for rental in rentals:
        data.append({
            'id': rental.id,
            'book_id': rental.book_id,
            'book_title': rental.book.title,
            'rental_date': rental.rental_date,
            'return_date': rental.return_date,
            'returned': rental.returned
        })
    return jsonify(data)

@app.route('/api/rentals/<int:rental_id>', methods=['GET'])
def api_get_rental(rental_id):
    rental = Rentals.query.get_or_404(rental_id)
    data = {
        'id': rental.id,
        'book_id': rental.book_id,
        'book_title': rental.book.title,
        'rental_date': rental.rental_date,
        'return_date': rental.return_date,
        'returned': rental.returned
    }
    return jsonify(data)

@app.route('/api/rentals', methods=['POST'])
def api_add_rental():
    data = request.json
    book_id = data.get('book_id')
    rental_date = data.get('rental_date', str(date.today()))
    returned = data.get('returned', False)

    rental = Rentals(book_id=book_id, rental_date=rental_date, returned=returned)
    db.session.add(rental)
    db.session.commit()

    return jsonify({'message': 'Rental added', 'rental_id': rental.id}), 201

@app.route('/api/rentals/<int:rental_id>', methods=['PUT'])
def api_update_rental(rental_id):
    rental = Rentals.query.get_or_404(rental_id)
    data = request.json
    if 'book_id' in data:
        rental.book_id = data['book_id']
    if 'rental_date' in data:
        rental.rental_date = data['rental_date']
    if 'return_date' in data:
        rental.return_date = data['return_date']
    if 'returned' in data:
        rental.returned = data['returned']
    db.session.commit()
    return jsonify({
        'message': 'Rental updated',
        'rental': {
            'id': rental.id,
            'book_id': rental.book_id,
            'book_title': rental.book.title,
            'rental_date': rental.rental_date,
            'return_date': rental.return_date,
            'returned': rental.returned
        }
    })

@app.route('/api/rentals/<int:rental_id>', methods=['DELETE'])
def api_delete_rental(rental_id):
    rental = Rentals.query.get_or_404(rental_id)
    db.session.delete(rental)
    db.session.commit()
    return jsonify({'message': 'Rental deleted'})


# Uruchomienie aplikacji
if __name__ == "__main__":
    app.run(debug=True)
