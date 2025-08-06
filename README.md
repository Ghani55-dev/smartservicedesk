
# Smart ServiceDesk - Django Project Documentation

## Project Overview

Smart ServiceDesk is a Django-based ticketing system designed to manage customer support efficiently. It includes three types of user roles: **Admin**, **Agent**, and **Customer**. The system allows customers to raise tickets, admins to assign them to agents, and agents to update ticket statuses.

---

## Features

- User Authentication (Login/Logout/Register)
- Custom User Roles: Admin, Agent, Customer
- Only Customers can self-register
- Admin creates Agents and Admins via Django Admin
- Ticket Creation (Customers)
- Ticket Assignment (Admins)
- Ticket Status Update (Agents)
- Email Notifications (HTML emails)
- Activity Logging
- Dashboard for each user role
- Mobile-responsive UI

---

## Tech Stack

- **Backend**: Django 5.2
- **Frontend**: Django Templates, Bootstrap 5
- **Database**: SQLite (dev), PostgreSQL (production)
- **Deployment**: Render.com
- **Email**: SMTP (Gmail)

---

## User Roles and Permissions

| Role     | Can Create Ticket | Can Assign Ticket | Can Update Status |
| -------- | ----------------- | ----------------- | ----------------- |
| Customer | Yes               | No                | No                |
| Agent    | No                | No                | Yes (Assigned)    |
| Admin    | No                | Yes               | No                |

---

## App Structure

```
smartservicedesk/
├── core/               # User Auth, Dashboard
├── tickets/            # Ticket logic, forms, views, utils
├── templates/
│   ├── core/
│   └── tickets/
├── static/             # CSS/JS
├── utils.py            # Email sending logic
├── settings.py         # Configurations
└── urls.py             # Routing
```

---

## Installation (Local)

```bash
git clone https://github.com/yourname/smartservicedesk.git
cd smartservicedesk
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Deployment (Render.com)

1. Push to GitHub repo
2. Create new web service on [Render](https://render.com/)
3. Set environment variables:
   - `DEBUG=False`
   - `SECRET_KEY=your-secret-key`
   - `ALLOWED_HOSTS=smartservicedesk.onrender.com`
   - Email Settings (SMTP)
4. Add `build.sh`:

```bash
#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
```

5. Add `render.yaml` (optional)
6. Deploy and verify static files, email, routes

---

## Email Notification Logic

File: `utils.py`

```python
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_ticket_notification(subject, template, context, recipient):
    message = render_to_string(template, context)
    send_mail(
        subject,
        '',  # Plaintext fallback (empty)
        'no-reply@smartdesk.com',
        [recipient],
        html_message=message,
        fail_silently=True
    )
```

Example usage:

```python
send_ticket_notification(
    subject="New Ticket Assigned",
    template="emails/ticket_assigned.html",
    context={"ticket": ticket},
    recipient=ticket.assigned_to.email
)
```

---

## Security Considerations

- DEBUG = False in production
- SECRET_KEY and sensitive info via environment variables
- Only customers register via UI
- Admin assigns roles and manages users
- CSRF protection enabled

---

## Future Enhancements

- PDF Export for tickets
- Advanced Search/Filter
- Chat Support with WebSockets
- Role-based dashboards
- API with DRF
- Mobile App (Flutter/React Native)

---

## Live Project

🌐 [https://smartservicedesk.onrender.com](https://smartservicedesk.onrender.com)

---

## Author

**Ghani**  
Full Stack Developer & DevOps Enthusiast

For questions/support: [ghani@example.com](mailto:ghani@example.com)
