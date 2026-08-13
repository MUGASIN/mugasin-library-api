# mugasin-library-api

Django REST API for the Library Lending System.

## Tech Stack
- Python / Django 6.1
- Django REST Framework
- PostgreSQL
- django-cors-headers

## Prerequisites
- Python 3.10+
- PostgreSQL installed and running

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/MUGASIN/mugasin-library-api.git
cd mugasin-library-api
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install django djangorestframework psycopg2-binary django-cors-headers
```

### 4. PostgreSQL Setup
Open psql and run:
```sql
CREATE DATABASE library_db;
```

### 5. Configure environment
Open `library_project/settings.py` and update DATABASES:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Start the server
```bash
python manage.py runserver
```

API runs at: `http://127.0.0.1:8000`

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/books/ | List all books |
| POST | /api/books/create/ | Add a new book |
| GET | /api/books/{id}/ | Get book details |

## Book Fields
- title (required)
- author (required)
- isbn (required, unique)
- category
- publication_year (required, 1000–2026)
- is_active (default: true)

## Validations
- Title, Author, ISBN are required
- Publication year must be between 1000 and current year
- ISBN must be unique

## Assumptions
- No authentication required for this version
- CORS is open for all origins (development only)
- SQLite removed; PostgreSQL is required