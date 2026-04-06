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
- **Authentication:** JWT (SimpleJWT)
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

- JWT token authentication (access + refresh tokens)
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

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

**Login:** `POST /api/token/` with username and password to receive an access token and a refresh token.

**Authenticated requests:** Include the access token in the Authorization header as `Bearer <token>`.

**Token refresh:** `POST /api/token/refresh/` with the refresh token to get a new access token when the current one expires.

Access tokens expire after 1 hour. Refresh tokens expire after 7 days.

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

## Testing Guide

This guide walks through testing every API endpoint using the Swagger UI at `/api/docs/` or any API client like Postman.

### Step 1: Get an Admin Token

```
POST /api/token/
{
    "username": "your-admin-username",
    "password": "your-admin-password"
}
```

Copy the `access` token from the response. In Swagger UI, click the "Authorize" button at the top and enter: `Bearer <your-access-token>`.

### Step 2: Test User Management (Admin only)

**Create users with different roles:**

```
POST /api/users/
{
    "username": "analyst_user",
    "email": "analyst@example.com",
    "password": "testpass123",
    "role": "Analyst"
}
```

```
POST /api/users/
{
    "username": "viewer_user",
    "email": "viewer@example.com",
    "password": "testpass123",
    "role": "Viewer"
}
```

**List all users:**
```
GET /api/users/
```

**Get a specific user:**
```
GET /api/users/2/
```

**Update a user:**
```
PATCH /api/users/2/
{
    "role": "Analyst"
}
```

**Delete a user:**
```
DELETE /api/users/3/
```

### Step 3: Test Transactions (as Admin)

**Create transactions:**

```
POST /api/transactions/
{
    "amount": 50000.00,
    "type_of": "Income",
    "category": "salary",
    "notes": "March salary"
}
```

```
POST /api/transactions/
{
    "amount": 15000.00,
    "type_of": "Expense",
    "category": "rent",
    "notes": "March rent"
}
```

```
POST /api/transactions/
{
    "amount": 3000.00,
    "type_of": "Expense",
    "category": "food",
    "notes": "Groceries"
}
```

**List all transactions:**
```
GET /api/transactions/
```

**Filter transactions:**
```
GET /api/transactions/?type_of=Income
GET /api/transactions/?category=food
GET /api/transactions/?start_date=2025-01-01&end_date=2025-12-31
```

**Search transactions:**
```
GET /api/transactions/?search=rent
```

**Update a transaction:**
```
PATCH /api/transactions/1/
{
    "amount": 55000.00,
    "notes": "March salary - revised"
}
```

**Delete a transaction (soft delete):**
```
DELETE /api/transactions/3/
```

### Step 4: Test Dashboard

**View full dashboard:**
```
GET /api/dashboard/
```

Expected response includes total_income, total_expenses, net_balance, category_totals, recent_transactions, and monthly_trends.

**View a specific user's dashboard:**
```
GET /api/dashboard/?user_id=2
```

### Step 5: Test Access Control

**Login as Analyst:**
```
POST /api/token/
{
    "username": "analyst_user",
    "password": "testpass123"
}
```

Use the new token and verify:
- ✅ `GET /api/transactions/` — should work
- ✅ `GET /api/dashboard/` — should work
- ❌ `POST /api/transactions/` — should return 403 Forbidden
- ❌ `GET /api/users/` — should return 403 Forbidden

**Login as Viewer:**
```
POST /api/token/
{
    "username": "viewer_user",
    "password": "testpass123"
}
```

Use the new token and verify:
- ✅ `GET /api/dashboard/` — should work (own data only)
- ❌ `GET /api/transactions/` — should return 403 Forbidden
- ❌ `POST /api/transactions/` — should return 403 Forbidden
- ❌ `GET /api/users/` — should return 403 Forbidden
- ❌ `GET /api/dashboard/?user_id=1` — should ignore the parameter and show only own data

### Step 6: Test Validation

**Invalid amount:**
```
POST /api/transactions/
{
    "amount": -500,
    "type_of": "Income",
    "category": "salary"
}
```
Expected: 400 Bad Request with "Amount must be greater than zero."

**Missing required fields:**
```
POST /api/transactions/
{
    "notes": "just a note"
}
```
Expected: 400 Bad Request with field-level errors.

**Invalid category:**
```
POST /api/transactions/
{
    "amount": 1000,
    "type_of": "Income",
    "category": "invalid_category"
}
```
Expected: 400 Bad Request.

### Step 7: Test Without Authentication

Remove the Authorization header and try:
```
GET /api/transactions/
```
Expected: 401 Unauthorized.

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
- **JWT for authentication:** Stateless token-based auth makes the API suitable for consumption by frontends and mobile apps. Session auth is retained alongside for the browsable API during development.
- **Superuser bypass:** Django superusers are granted full access in permission checks to avoid lockout scenarios.
- **Analyst sees all data by default:** Analysts have a bird's-eye view of all transactions and summaries, with the option to drill down to a specific user via `?user_id=`. This differentiates them from Viewers who only see their own data.
- **No tokens on registration:** User creation is admin-only, so the new user logs in separately to get their own tokens.

---

## Error Handling

The API returns appropriate HTTP status codes:

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request / validation error |
| 401 | Unauthorized (not logged in or invalid token) |
| 403 | Forbidden (insufficient role) |
| 404 | Not found |
| 429 | Rate limit exceeded |

---

## Rate Limiting

| User Type | Limit |
|-----------|-------|
| Anonymous | 20 requests/hour |
| Authenticated | 100 requests/hour |