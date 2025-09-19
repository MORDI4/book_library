from datetime import date
from library import app
from app.models import db,Authors, Books, Rentals

with app.app_context():  # <<<<< to jest kluczowe
    # Tworzymy tabelki, jeśli jeszcze ich nie ma
    db.create_all()

    # Autorzy
    author1 = Authors(name="Adam", surname="Mickiewicz", birth_year=date(1798, 12, 24))
    author2 = Authors(name="Henryk", surname="Sienkiewicz", birth_year=date(1846, 5, 5))
    author3 = Authors(name="Juliusz", surname="Słowacki", birth_year=date(1809, 9, 4))

    db.session.add_all([author1, author2, author3])
    db.session.commit()

    # Książki
    book1 = Books(
        title="Pan Tadeusz",
        description="Epopeja narodowa",
        genre="Poetry",
        year_published=1834,
        authors=[author1]
    )
    book2 = Books(
        title="Ogniem i Mieczem",
        description="Historyczna powieść przygodowa",
        genre="Historical Novel",
        year_published=1884,
        authors=[author2]
    )
    db.session.add_all([book1, book2])
    db.session.commit()

    # Wypożyczenia
    rental = Rentals(book_id=book1.id, rental_date=date(2025, 9, 1), returned=False)
    db.session.add(rental)
    db.session.commit()

    print("📚 Testowe dane dodane!")
