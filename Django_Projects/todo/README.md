# Task Manager

[![python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)](.)
[![django](https://img.shields.io/badge/Django-5.0-092E20?style=flat-square&logo=django&logoColor=white)](.)
[![sqlite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](.)
[![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)](.)

> Small Django app: sign up, log in, keep a private list of tasks. Bootstrap 5, SQLite. Practice project, not a SaaS.

---

## What it does

A logged-in user can add / edit / delete tasks and toggle Pending ↔ Completed. The list on Home is **that user only**. Filter by status on View Tasks.

| | |
| --- | --- |
| Auth | Django `User`. Sign up needs matching passwords. `login_required` on every task page. |
| Tasks | `task_name`, `description`, `status` (`Pending` / `Completed`), `owner`, `created_at` |
| UI | Bootstrap 5. Add / edit in a modal. Delete is a **POST** (not a GET link). |
| Tests | 6 cases — login redirect, isolation, add, foreign delete 404, status toggle, signup |

This is CRUD + auth. No reminders, no teams, no REST API.

---

## How to run

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) — that sends you to login. Sign up first.

```bash
python manage.py test
```

`db.sqlite3` is created on migrate. It is gitignored. Do not commit a database with real passwords in it.

---

## Layout

```text
README.md
requirements.txt
manage.py
todo/settings.py          project settings
app/models.py             Task
app/views.py
app/forms.py
app/urls.py
app/templates/            Bootstrap pages
static/assets/css/
```

Drop this folder in as `Django_Projects/todo/` on GitHub.

---

## Notes I actually hit

- Unauthenticated `/index/` used to bounce to `/accounts/login/`, which did not exist. `LOGIN_URL` is now `login`.
- Tasks used to be a single global table. They are per `owner` now. Bob cannot see or delete Alice's row (the test checks 404).
- Delete used to be a GET `<a href>`. It is a POST form.
- `SECRET_KEY` is `DJANGO_SECRET_KEY` or a **dev-only** fallback. Do not use the fallback on a public host.
- Signup uses Django's password validators (min length, not all-numeric, etc.).

---

## License

MIT. Bootstrap / Boxicons / Font Awesome stay with their CDNs.
