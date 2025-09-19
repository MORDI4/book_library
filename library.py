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

@app.route('/edit/<int:book_id>')
def edit(book_id):
    return redirect(url_for("main_page"))

@app.route('/delete/<int:book_id>')
def delete(book_id):
    return redirect(url_for("main_page"))

# Uruchomienie aplikacji
if __name__ == "__main__":
    app.run(debug=True)
