# Finance Dashboard Backend API

A Django REST Framework backend for a finance dashboard system with role-based access control, financial record management, and analytics.

## Live Demo

**Deployed URL:** `https://your-username.pythonanywhere.com`

| Endpoint | URL |
|----------|-----|
| API Root | `/api/` |
| Swagger Docs | `/api/docs/` |
| Admin Panel | `/admin/` |

Full interactive API documentation is available at the Swagger UI link above.

---

## Tech Stack

- **Language:** Python 3.10
- **Framework:** Django 5.2, Django REST Framework
- **Database:** SQLite
- **Documentation:** drf-spectacular (Swagger/OpenAPI)
- **Filtering:** django-filter
- **Deployment:** PythonAnywhere

---

## Features

### Core

- User and role management (Admin, Analyst, Viewer)
- Financial record CRUD (income/expense transactions)
- Dashboard summary with analytics and monthly trends
- Role-based access control at every endpoint
- Filtering, searching, and pagination

### Additional

- Interactive API documentation (Swagger UI)
- Pagination (10 items per page)
- Search support across notes and categories
- Soft delete for transactions
- Rate limiting (20/hr anonymous, 100/hr authenticated)
- Custom admin panel restricted to Admin role users

---

## Role-Based Access Control

The system enforces three user roles with distinct permissions:

| Action | Viewer | Analyst | Admin |
|--------|--------|---------|-------|
| View dashboard (own data) | ✅ | ✅ | ✅ |
| View dashboard (all data) | ❌ | ✅ | ✅ |
| View dashboard (specific user) | ❌ | ✅ | ✅ |
| View transactions | ❌ | ✅ | ✅ |
| Create/update/delete transactions | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |
| Access admin panel | ❌ | ❌ | ✅ |

---

## Data Models

### User

Extends Django's `AbstractUser` with custom fields:

| Field | Type | Description |
|-------|------|-------------|
| username | string | Unique username (inherited) |
| email | string | Email address (inherited) |
| password | string | Hashed password (inherited) |
| role | enum | `Viewer`, `Analyst`, or `Admin` (default: Viewer) |
| isactive | boolean | Whether the user account is active (default: true) |

### Transaction

| Field | Type | Description |
|-------|------|-------------|
| user | FK → User | The user who created the record |
| amount | decimal | Transaction amount (max 12 digits, 2 decimal places) |
| type_of | enum | `Income` or `Expense` |
| category | enum | `salary`, `freelance`, `investment`, `rent`, `food`, `utilities`, `entertainment`, `healthcare`, `transport`, `other` |
| notes | string | Optional description (max 255 chars) |
| date | datetime | Auto-set on creation |
| is_deleted | boolean | Soft delete flag (default: false) |
| created_at | datetime | Auto-set on creation |
| updated_at | datetime | Auto-updated on save |

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- pip

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser:**
```bash
python manage.py createsuperuser
```

6. **Set the superuser role to Admin:**
```bash
python manage.py shell
```
```python
from api.models import User
user = User.objects.get(username='your-username')
user.role = 'Admin'
user.save()
exit()
```

7. **Run the development server:**
```bash
python manage.py runserver
```

8. **Access the application:**
    - API: http://localhost:8000/api/
    - Swagger Docs: http://localhost:8000/api/docs/
    - Admin Panel: http://localhost:8000/admin/

---

## Project Structure

```
project-root/
├── your_project_name/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── models.py          # User and Transaction models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # ViewSets and APIViews
│   ├── permissions.py      # Custom permission classes
│   ├── filters.py          # django-filter FilterSets
│   ├── admin.py            # Custom admin site configuration
│   └── urls.py             # App-level URL routing
├── requirements.txt
├── manage.py
└── README.md
```

---

## Assumptions & Design Decisions

- **Category as enum, not a separate model:** Categories are defined as `TextChoices` on the Transaction model for simplicity. A separate Category model could be used for dynamic category management but was deemed unnecessary for this scope.
- **Soft delete over hard delete:** Transactions are soft-deleted (marked with `is_deleted=True`) rather than removed from the database, allowing data recovery.
- **Date auto-set on creation:** The `date` field uses `auto_now_add=True`, meaning it captures when the record was created. A manual date field could be added if backdating transactions is needed.
- **SQLite for simplicity:** SQLite is used as the database for ease of setup and deployment. For production at scale, PostgreSQL would be recommended.
- **Superuser bypass:** Django superusers are granted full access in permission checks to avoid lockout scenarios.
- **Analyst sees all data by default:** Analysts have a bird's-eye view of all transactions and summaries, with the option to drill down to a specific user via `?user_id=`. This differentiates them from Viewers who only see their own data.

---

## Error Handling

The API returns appropriate HTTP status codes:

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request / validation error |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (insufficient role) |
| 404 | Not found |
| 429 | Rate limit exceeded |

Validation errors return descriptive messages:
```json
{
    "amount": ["Amount must be greater than zero."]
}
```

---

## Rate Limiting

| User Type | Limit |
|-----------|-------|
| Anonymous | 20 requests/hour |
| Authenticated | 100 requests/hour |
