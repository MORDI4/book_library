from datetime import date
from library import app
from app.models import db,Authors, Books, Rentals

with app.app_context(): 
    db.session.query(Rentals).delete()

    # Zatwierdzamy zmiany
    db.session.commit()

