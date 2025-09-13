from app import app, db
from app.models import Authors, Books, Rentals

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Author": Authors,
        "Book": Books,
        "Rental": Rentals
    }