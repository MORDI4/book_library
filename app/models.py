from app import db

books_authors = db.Table(
    'books_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True, unique=True, nullable=False)
    description = db.Column(db.String(300))
    genre = db.Column(db.String(200), index=True)
    year_published = db.Column(db.Integer, index=True)
    authors = db.relationship(
            'Authors', 
            secondary=books_authors, 
            backref=db.backref('books', lazy='dynamic')
        )
    rentals = db.relationship('Rentals', backref='books', lazy='dynamic')

    def __str__(self):
        return f'<Book {self.id} - {self.title}>'
    
class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), index=True, nullable=False)
    birth_year = db.Column(db.Date)

    def __str__(self):
        return f'<Author {self.id} - {self.name} {self.surname}>'


class Rentals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), index=True, nullable=False)
    rental_date = db.Column(db.Date, index=True, nullable=False)
    return_date = db.Column(db.Date, index=True)
    returned = db.Column(db.Boolean, nullable=False, default=False)

    def __str__(self):
        return f'<Rental {self.id} - Book {self.book_id} {'returned' if self.returned else 'rented'}>'