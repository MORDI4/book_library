from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models import db, Books, Authors, Rentals
from app import create_app
from datetime import date


app = create_app()

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



# Uruchomienie aplikacji
if __name__ == "__main__":
    app.run(debug=True)
