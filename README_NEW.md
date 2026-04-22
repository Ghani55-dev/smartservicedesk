# Smart ServiceDesk

A modern, role‑based support ticketing system built on Django.  
Agents, admins and customers collaborate through a responsive web interface; notifications, activity logs and dashboards keep the workflow efficient.

---

## 📋 Project Overview

Smart ServiceDesk enables organisations to manage customer support tickets with three distinct user roles:

- **Customer** – raises tickets and views their status.
- **Agent** – works on tickets assigned by an admin.
- **Admin** – manages users, assigns tickets and oversees the system.

Customers register via the public form; admins and agents are created through the Django admin UI.  
The system sends HTML email notifications and records every ticket activity for auditing.

---

## 🚀 Features

- User registration/login/logout with role‑based access
- Custom roles: Admin, Agent, Customer
- Ticket creation, listing and detail views
- Admin ticket assignment
- Agent status updates
- Activity logging (recent activities API)
- HTML email notifications (SMTP)
- Dashboard pages for each role
- Static assets managed with `collectstatic`
- Mobile‑responsive templates using Bootstrap 5
- Deployable on Render.com (or any VPS/Cloud provider)

---

## 🛠 Tech Stack

| Layer        | Technology               |
|--------------|--------------------------|
| Backend      | Django 5.2               |
| Frontend     | Django Templates + Bootstrap 5 |
| Database     | SQLite (development) / PostgreSQL (production) |
| Caching      | Redis (optional)         |
| Authentication | Django sessions (CSRF‑protected) |
| Email        | SMTP (Gmail example)     |
| Deployment   | Render.com / AWS / VPS   |
| Containerisation | Docker (optional)    |

---

## ⚙️ Installation Steps

```bash
# clone and enter workspace
git clone https://github.com/yourname/smartservicedesk.git
cd smartservicedesk

# create & activate virtual environment
python -m venv env
# macOS/Linux
source env/bin/activate
# Windows
env\Scripts\activate

# install dependencies
pip install -r requirements.txt

# prepare database
python manage.py migrate
python manage.py createsuperuser      # create admin user

# run development server
python manage.py runserver
```

---

## 🔐 Environment Variables

Create a `.env` file at project root (illustrative values):

```
# core
DEBUG=True
SECRET_KEY=super-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# database (Postgres example)
DATABASE_URL=postgres://user:pass@localhost:5432/smartdesk

# email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=yourpassword
EMAIL_USE_TLS=True

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
```

Use `django-environ` or similar to load these values in `settings.py`.

---

## 🗄 Database Setup

1. Configure `DATABASES` in `settings.py` (see `.env`).
2. Run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. (Optional) Load fixtures or seed data.
4. Use `python manage.py dbshell` for direct inspection.

---

## 🖥 Running Locally

After installation:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and register as a customer or log in with the superuser.

---

## 🐳 Running with Docker (optional)

Create a `Dockerfile` along these lines:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "smartservicedesk.wsgi:application", "--bind", "0.0.0.0:8000"]
```

And a `docker-compose.yml`:

```yaml
version: "3.9"
services:
  web:
    build: .
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: smartdesk
  redis:
    image: redis:alpine
```

```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🚢 Deployment Instructions

### Render.com (example)

1. Push the repository to GitHub.
2. Create a new **Web Service** on Render.
3. Connect the GitHub repo and set branch to `main`.
4. Add the following environment variables in Render dashboard (mirror `.env`).
5. Set a `build` command:

   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

6. Set `Start Command` to:

   ```
   gunicorn smartservicedesk.wsgi
   ```

7. Deploy and test the application; ensure static files and email work.

### AWS / VPS / Other

- Provision a server/container.
- Install Python, PostgreSQL, Redis.
- Clone repo and follow installation steps.
- Use a process manager (systemd, supervisord) to run Gunicorn.
- Configure Nginx as a reverse proxy.

---

## 📁 Folder Structure Explanation

```
smartservicedesk/                # project root
├── core/                        # authentication, dashboard, static assets
│   ├── models.py                # User model (with role field)
│   ├── views.py                 # Login, register, dashboard
│   └── templates/core/          # HTML templates for core app
├── tickets/                     # ticketing logic
│   ├── models.py                # Ticket, TicketActivity
│   ├── views.py                 # create/list/detail, API
│   └── templates/tickets/       # ticket templates
├── smartservicedesk/            # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── static/                      # collected static assets
├── templates/                   # global templates
├── requirements.txt
├── manage.py
└── README_NEW.md
```

---

## 🌐 API Base URL

```
https://<your-domain>/
```

All endpoints are relative to this base.

---

## 🔑 Authentication Method

- Traditional Django session authentication.
- Login via `/` (POST with `username` + `password`).
- CSRF tokens required for form submissions.
- Protects all views with `@login_required`.

---

## ⚠ Error Handling Structure

- Views return standard HTTP status codes:
  - `403` for forbidden access (e.g. non‑customer creating ticket).
  - `404` for missing tickets/users.
  - Django form errors rendered back to templates.
  - JSON API returns 200 with error messages inside payload on failure.
- Middleware captures unhandled exceptions and shows friendly 500 page when `DEBUG=False`.

---

## 🤝 Contribution Guide

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/awesome`.
3. Install dependencies and run tests: `python manage.py test`.
4. Write clear commit messages.
5. Submit a pull request with a description of your changes.
6. Ensure code follows PEP 8 and passes linting (`flake8`/`black`).

---

## 📄 License

This project is released under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.
