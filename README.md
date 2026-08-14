# mugasin-library-api

Django REST API backend for the Library Lending System.

## Tech Stack
- Python 3.13
- Django 6.1
- Django REST Framework 3.18
- PostgreSQL
- django-cors-headers
- psycopg2-binary

## Prerequisites
- Python 3.10+
- PostgreSQL 
- pip

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/MUGASIN/mugasin-library-api.git
cd mugasin-library-api
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
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

### 5. Configure Database
Open `library_project/settings.py` and update DATABASES:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password', #password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
### 6. Run Migrations
```bash
python manage.py makemigration
python manage.py migrate
```
This will automatically:
- Create all required tables
- Migrate existing book records to the new BookCopy structure

### 7. Start the Server
```bash
python manage.py runserver
```
API runs at: `http://127.0.0.1:8000`

---

## Database Schema

### Book
| Field | Type | Description |
|-------|------|-------------|
| id | Serial | Primary key |
| title | VARCHAR(255) | Book title (required) |
| author | VARCHAR(255) | Book author (required) |
| isbn | VARCHAR(20) | Unique ISBN (required) |
| category | VARCHAR(100) | Book category |
| publication_year | INT | Year published (1000–2026) |
| is_active | BOOLEAN | Active status |
| created_at | TIMESTAMP | Record created time |
| updated_at | TIMESTAMP | Record updated time |

### BookCopy
| Field | Type | Description |
|-------|------|-------------|
| id | Serial | Primary key |
| book_id | FK→Book | Parent book |
| copy_number | VARCHAR(50) | Copy identifier (001, 002...) |
| status | VARCHAR(20) | available/borrowed/damaged/inactive |
| created_at | TIMESTAMP | Record created time |
| updated_at | TIMESTAMP | Record updated time |

### Member
| Field | Type | Description |
|-------|------|-------------|
| id | Serial | Primary key |
| name | VARCHAR(255) | Member name (required) |
| email | EmailField | Unique email (required) |
| joined_date | DATE | Auto set on creation |
| is_active | BOOLEAN | Active status |
| created_at | TIMESTAMP | Record created time |
| updated_at | TIMESTAMP | Record updated time |

### BorrowRecord
| Field | Type | Description |
|-------|------|-------------|
| id | Serial | Primary key |
| member_id | FK→Member | Who borrowed |
| book_copy_id | FK→BookCopy | Which copy |
| borrowed_at | TIMESTAMP | When borrowed |
| returned_at | TIMESTAMP | When returned (null if not) |
| is_returned | BOOLEAN | Return status |

---

## API Endpoints

### Books
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/books/ | List all books |
| GET | /api/books/?search=xyz | Search by title/author/ISBN |
| GET | /api/books/?status=active | Filter by active/inactive/all |
| POST | /api/books/create/ | Add a new book |
| GET | /api/books/{id}/ | Get book details |
| PUT | /api/books/{id}/ | Edit a book |

### Book Copies
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/books/{id}/copies/ | List copies of a book |
| POST | /api/books/{id}/copies/ | Add a copy to a book |

### Members
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/members/ | List all members |
| GET | /api/members/?search=xyz | Search by name/email |
| GET | /api/members/?status=active | Filter by active/inactive/all |
| POST | /api/members/create/ | Add a new member |
| GET | /api/members/{id}/ | Get member details |
| PUT | /api/members/{id}/ | Edit a member |

### Borrow & Return
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/borrow/ | Borrow a book copy |
| POST | /api/return/{record_id}/ | Return a borrowed book |
| GET | /api/borrow/history/ | Full borrow history |
| GET | /api/borrow/history/?member_id=x | Member borrow history |

---

## Business Rules
- Title, Author, ISBN are required when adding a book
- Publication year must be between 1000 and current year
- ISBN must be unique across all books
- Same title + author combination is not allowed
- Only active members can borrow books
- A book copy must be available before it can be borrowed
- A borrowed copy cannot be borrowed again until returned
- Borrowing history is never deleted
- Concurrent borrowing is protected using PostgreSQL row-level locking

## Assumptions
- Each new book automatically gets Copy 001 on creation
- Additional copies must be added via API
- CORS is open for all origins (development only)
- No authentication required for this version

## Known Limitations
- No authentication or authorization
- API URL must be updated for production deployment
- CORS should be restricted in production