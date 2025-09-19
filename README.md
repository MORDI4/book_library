# 📚 Book Library

Aplikacja webowa do zarządzania biblioteką książek — umożliwia dodawanie, edytowanie, usuwanie książek oraz śledzenie wypożyczeń. Zbudowana z użyciem Pythona, Flask i SQLAlchemy.

---

## 🧪 Technologie

- **Backend**: Python 3.10+
- **Framework**: Flask
- **Baza danych**: SQLite (z możliwością rozwoju na PostgreSQL)
- **ORM**: SQLAlchemy
- **Frontend**: HTML, Jinja2, Bootstrap 5

---

## 🚀 Instalacja

1. **Sklonuj repozytorium**:

    ```bash
    git clone https://github.com/MORDI4/book_library.git
    cd book_library

2. **Utwórz i aktywuj wirtualne środowisko**:

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/MacOS
    source venv/bin/activate


3. **Zainstaluj zależności**:

    ```bash
    pip install -r requirements.txt


4. **Skonfiguruj plik .flaskenv**:
Utwórz plik .flaskenv w katalogu głównym z następującą zawartością:

    ```bash
    FLASK_APP=library.py
    FLASK_ENV=development

5. **Zainicjalizuj migracje bazy danych**:

    ```bash
    flask db init # tylko przy pierwszym uruchomieniu projektu
    flask db migrate -m "Initial migration"
    flask db upgrade

6. **Uruchom aplikację**:

    ```bash
    flask run
    
Aplikacja będzie dostępna pod adresem: http://127.0.0.1:5000

---

## 📋 Funkcjonalności

- **Książki**:
  - Dodawanie nowych książek
  - Edytowanie istniejących książek
  - Usuwanie książek
  - Przeglądanie listy książek z informacjami o tytule, autorze, roku wydania, gatunku, opisie i statusie (wypożyczona/dostępna)

- **Wypożyczenia**:
  - Dodawanie nowych wypożyczeń
  - Aktualizowanie daty zwrotu
  - Przeglądanie historii wypożyczeń

---