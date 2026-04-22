# API Documentation for Smart ServiceDesk

> The application is primarily HTML‑based; only one JSON endpoint exists.  
> nevertheless, we document every public route for clarity.

### 1. **User Registration**

- **Method**: `GET` / `POST`  
- **URL**: `/register/`  
- **Headers**: `Content-Type: application/x-www-form-urlencoded`  
- **Payload (POST)**:

```json
{
  "username": "jdoe",
  "email": "jdoe@example.com",
  "password1": "secret123",
  "password2": "secret123"
}
```

- **Success (201/redirect)**:  
  - Redirects to login page with success message.
- **Errors**:
  - 400 – form validation errors (password mismatch, duplicate username).

> *Field descriptions*:  
> `username` – unique login name  
> `email` – valid email address  
> `password1/password2` – must match; follow Django’s password rules.

**cURL Example**:

```bash
curl -X POST https://<your-domain>/register/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=jdoe&email=jdoe@example.com&password1=secret123&password2=secret123"
```

---

### 2. **Login**

- **Method**: `GET` / `POST`  
- **URL**: `/`  
- **Headers**: `Content-Type: application/x-www-form-urlencoded`  
- **Payload (POST)**:

```json
{
  "username": "jdoe",
  "password": "secret123"
}
```

- **Success**: redirect to `/dashboard/`.  
- **Errors**:  
  - 401 – invalid credentials (rendered on same page).

**cURL Example**:

```bash
curl -c cookies.txt -X POST https://<your-domain>/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=jdoe&password=secret123"
```

---

### 3. **Logout**

- **Method**: `GET`  
- **URL**: `/logout/`  
- **Headers**: none required.  
- **Success**: redirects to login page.

**cURL Example**:

```bash
curl -b cookies.txt https://<your-domain>/logout/
```

---

### 4. **Dashboard**

- **Method**: `GET`  
- **URL**: `/dashboard/`  
- **Headers**: session cookie required.  
- **Success**: renders the appropriate dashboard for the user's role.

---

### 5. **Ticket Creation**

- **Method**: `GET` / `POST`  
- **URL**: `/tickets/create/`  
- **Headers**: session cookie, CSRF token  
- **Payload (POST)**:

```json
{
  "title": "Printer issue",
  "description": "Office printer jammed.",
  "priority": "medium"
}
```

- **Success**: redirect to `/tickets/list/` with message.  
- **Errors**:
  - 403 – if user is not a customer.
  - 400 – form validation errors.

> *Field descriptions*: `title` (string), `description` (text), `priority` ("low"|"medium"|"high").

**cURL Example** (simulating CSRF):

```bash
curl -b cookies.txt -c cookies.txt -X POST https://<your-domain>/tickets/create/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=Printer+issue&description=Office+printer+jammed.&priority=medium&csrfmiddlewaretoken=<token>"
```

---

### 6. **Ticket List**

- **Method**: `GET`  
- **URL**: `/tickets/list/`  
- **Headers**: authenticated session.  
- **Success**: HTML page listing tickets according to role:
  - Admin: all tickets
  - Agent: tickets assigned to them
  - Customer: own tickets

---

### 7. **Ticket Detail / Update**

- **Method**: `GET` / `POST`  
- **URL**: `/tickets/<int:ticket_id>/`  
- **Headers**: session, CSRF  
- **Payload (POST)** depends on role:

  - **Admin assignment**:

    ```json
    {
      "assign-assigned_to": 5
    }
    ```

  - **Agent status update**:

    ```json
    {
      "status-status": "resolved"
    }
    ```

- **Success**: redirect back to detail page with a flash message.  
- **Errors**:
  - 403 – forbidden action (e.g. non‑admin trying to assign).
  - 404 – ticket not found.
  - 400 – invalid form submission.

---

### 8. **Recent Activities API**

- **Endpoint Name**: Recent Ticket Activities  
- **Method**: `GET`  
- **URL**: `/tickets/api/recent-activities/`  
- **Headers**: session cookie required.  
- **Request Payload**: _none_

- **Success Response (200)**:

```json
{
  "activities": [
    {
      "ticket_id": 12,
      "action": "status updated to 'closed'",
      "user": "agent_jane",
      "time_ago": "3 minutes ago"
    },
    ...
  ]
}
```

- **Error Responses**:

| Code | Description |
|------|-------------|
| 401  | Not authenticated |
| 403  | CSRF token missing/invalid |
| 500  | Internal server error |

**cURL Example**:

```bash
curl -b cookies.txt https://<your-domain>/tickets/api/recent-activities/
```

---

### 9. **Static and Informational Pages**

| Path                  | Method | Description                        |
|-----------------------|--------|------------------------------------|
| `/privacy-policy/`    | GET    | Privacy policy text                |
| `/terms-of-service/`  | GET    | Terms of service text              |
| `/contact/`           | GET/POST | Contact form (email)            |

---

> ⚠ **Note**: All HTML endpoints require CSRF tokens when using POST.  
> There is currently no RESTful API for ticket CRUD beyond the `/api/recent-activities/` route; extending the project with Django REST Framework is a planned enhancement.
