# Track My Funds

**FinanceTrack** is a robust and user-friendly web application built with the Django framework designed to help users efficiently manage their personal or small business finances. The application allows users to record their income and expenses, add new transactions, set and track budgets, and generate detailed financial reports to analyze their financial health.

---

## Key Features

- **Add Transactions:** Easily add daily income and expense transactions.
- **Dashboard View:** Clean and dynamic dashboard displaying total income, total expenses, and current balance.
- **Budgeting:** Set monthly or yearly budgets and monitor spending against these budgets.
- **Financial Reports:** Generate detailed reports including monthly/yearly expense analysis, category-wise spending, and income sources.
- **Role-based Access (Optional):** Supports multiple users with role-based permissions for enhanced security.
- **Responsive Design:** Built with Bootstrap 5 for seamless use across mobile and desktop devices.

---

## Technologies Used

- **Backend:** Django Framework (Python)
- **Frontend:** Django Templates, Bootstrap 5
- **Database:** SQLite (default) / PostgreSQL (optional for production)
- **Additional Libraries:**
  - Chart.js for financial data visualization
  - Django Forms for input validation
  - anime.js for UI animations

---

## Installation & Setup

### Prerequisites

- Python 3.8 or above
- Git (optional)
- Virtual Environment tool (venv or virtualenv)

### Steps

1. **Clone the repository** (if using Git):
   ```bash
   git clone <your-repo-url>
   cd <project-folder>



## Create a virtual environment and activate it:
- python3 -m venv venv
- source venv/bin/activate  # Linux/Mac
- venv\Scripts\activate     # Windows


##  Install dependencies from requirements.txt:

pip install -r requirements.txt


## Set up environment variables:

- SECRET_KEY=your_secret_key_here
- DEBUG=True
- DATABASE_URL=sqlite:///db.sqlite3


## Apply migrations:

python manage.py makemigrations
python manage.py migrate


## Run the development server:
python manage.py runserver


# File Tree: innobyte

```
├── 📁 .vscode/ 🚫 (auto-hidden)
├── 📁 core/
│   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   ├── 📁 migrations/
│   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   ├── 🐍 0001_initial.py
│   │   ├── 🐍 0002_customuser_fullname.py
│   │   ├── 🐍 0003_alter_customuser_email.py
│   │   ├── 🐍 0004_alter_customuser_email.py
│   │   ├── 🐍 0005_transaction.py
│   │   ├── 🐍 0006_transaction_type.py
│   │   ├── 🐍 0007_transaction_user.py
│   │   ├── 🐍 0008_remove_transaction_user_alter_customuser_fullname_and_more.py
│   │   ├── 🐍 0009_transaction_user.py
│   │   ├── 🐍 0010_remove_transaction_description_transaction_title_and_more.py
│   │   ├── 🐍 0011_alter_transaction_user.py
│   │   ├── 🐍 0012_rename_title_transaction_description.py
│   │   ├── 🐍 0013_remove_transaction_type.py
│   │   ├── 🐍 0014_category_budget.py
│   │   └── 🐍 __init__.py
│   ├── 📁 templates/
│   │   ├── 🌐 add_transaction.html
│   │   ├── 🌐 base.html
│   │   ├── 🌐 budgeting.html
│   │   ├── 🌐 dashboard.html
│   │   ├── 🌐 financial_reports.html
│   │   ├── 🌐 forget_password.html 🚫 (auto-hidden)
│   │   ├── 🌐 login_page.html
│   │   └── 🌐 signup.html
│   ├── 📁 templatetags/
│   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   ├── 🐍  __init__.py
│   │   └── 🐍 extra_filters.py
│   ├── 🐍 __init__.py
│   ├── 🐍 admin.py
│   ├── 🐍 apps.py
│   ├── 🐍 models.py
│   ├── 🐍 tests.py
│   ├── 🐍 urls.py
│   └── 🐍 views.py
├── 📁 innobyte/
│   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   ├── 🐍 __init__.py
│   ├── 🐍 asgi.py
│   ├── 🐍 settings.py
│   ├── 🐍 urls.py
│   └── 🐍 wsgi.py
├── 📁 myvirtual/
│   ├── 📁 bin/ 🚫 (auto-hidden)
│   ├── 📁 include/
│   │   └── 📁 python3.12/
│   ├── 📁 lib/ 🚫 (auto-hidden)
│   ├── 📄 lib64
│   └── ⚙️ pyvenv.cfg
├── 📄 .env  
├── 📖 README.md
├── 📄 client_secret.json
├── 📄 db.sqlite3
├── 🐍 manage.py
└── 📄 requirements.txt 🚫 (auto-hidden)
```

