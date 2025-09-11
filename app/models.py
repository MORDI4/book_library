from app import db

class Books(db.Model):
    id = db.Column(db.Integer, primarykey=True)
    title = db.Column(db.String(200), index=True, unique=True, nullable=False)
    author_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    descpription = db.Column(db.String(300))
    genre = db.Column(db.String(200), index=True)
    year_published = db.Column(db.Integer, index=True)

    def __str__(self):
        return f'<Book {self.id} - {self.title}>'
    
class Authors(db.Model):
    id = db.Column(db.Integer, primarykey=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), index=True, nullable=False)
    birth_year = db.Column(db.Date)


class Rentals(db.Model):
    id = db.Column(db.Integer, primarykey=True)
    book_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    rental_date = db.Column(db.Date, index=True, nullable=False)
    return_date = db.Column(db.Date, index=True)
    returned = db.Column(db.Boolean)