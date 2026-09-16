# Request Management System

[![python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)](.)
[![django](https://img.shields.io/badge/Django-5.0-092E20?style=flat-square&logo=django&logoColor=white)](.)
[![sqlite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](.)
[![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)](.)

> Django app: a user files a request, staff approve or reject it, an email goes out. Bootstrap 5, SQLite. Practice project.

---

## What it does

| Role | Can do |
| --- | --- |
| Regular user | Sign up, log in, submit a request, see **their** rows |
| Staff (`is_staff=True`) | Open `/adminpanel/`, filter pending / approved / rejected, POST approve or reject |

Approve and reject **write a status**. They also send mail. Mail defaults to the **console** so you can run this without Gmail.

| | |
| --- | --- |
| Model | `ServiceRequest`: name, phone, email, location, message, status, owner, timestamps |
| Status | `pending` → `approved` or `rejected` |
| Auth | `login_required` + `user_passes_test(is_staff)` on the panel |
| Tests | 5 cases — login wall, user blocked from panel, submit is pending, user cannot approve, staff approve sends mail |

This is not a ticket system. No SLAs, no attachments.

---

## How to run

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser    # this account is staff → admin panel
python manage.py runserver
```

[http://127.0.0.1:8000/](http://127.0.0.1:8000/) is login. Sign up a second account for the user side.

```bash
python manage.py test
```

### Optional: real SMTP

By default `EMAIL_BACKEND` prints to the terminal. To use Gmail (or any SMTP), put this in the environment — **not in the repo**:

```bash
export EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
export EMAIL_HOST_USER=you@gmail.com
export EMAIL_HOST_PASSWORD=app-password-here
export DEFAULT_FROM_EMAIL=you@gmail.com
export ADMIN_NOTIFY_EMAIL=you@gmail.com
```

If `ADMIN_NOTIFY_EMAIL` is empty, the “new request” mail is skipped. Approve / reject still mail the requester when a backend is configured.

Do not commit SMTP passwords. If an older copy of this project had a Gmail app password in `settings.py`, rotate that password.

SQLite is the database so the project runs with one command. MySQL is not required.

---

## Layout

```text
README.md
requirements.txt
manage.py
smtp1/settings.py
app1/models.py          ServiceRequest
app1/views.py
app1/forms.py
app1/templates/
static/assets/css/style.css
```

Drop this folder in as `Django_Projects/smtp1/` on GitHub.

---

## Notes I actually hit

- The panel used to list every row with no status column, so Approve did not change anything in the database. Status is stored now.
- Regular users used to be able to open `/adminpanel/`. They get bounced.
- Approve / reject are POST only.
- `SECRET_KEY` and mail credentials come from env vars, with a **dev-only** fallback for the key.

---

## License

MIT. Bootstrap stays on the CDN.
