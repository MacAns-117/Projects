# Hospital records

[![python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)](.)
[![django](https://img.shields.io/badge/Django-5.0-092E20?style=flat-square&logo=django&logoColor=white)](.)
[![sqlite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](.)
[![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)](.)

> One Django app for **patients** and **nurses**. Login, dashboard counts, CRUD, SQLite. Practice project — not a real hospital system.

The two assigned pieces (patient details + nurse list) live in the same project. One login, one nav, two models.

---

## What it does

| | Patients | Nurses |
| --- | --- | --- |
| Fields | name, blood group, age, disease, location | name, gender, department, shift, care, years, certs, phone, email, address, optional photo |
| List | filter by id or name | filter by department / shift |
| Write | add / edit / delete (POST) | add / edit / delete (POST) |

Every records page is `login_required`. Dashboard shows the two counts.

This is CRUD. No wards, no appointments, no billing.

---

## How to run

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

[http://127.0.0.1:8000/](http://127.0.0.1:8000/) → login. Sign up a normal account if you do not want the admin user.

```bash
python manage.py test
```

Nurse photos go in `media/nurse_pics/` (gitignored). Pillow is required because of `ImageField`.

---

## Layout

```text
README.md
requirements.txt
manage.py
HMS/settings.py
records/models.py          Patient, Nurse
records/views.py
records/forms.py
records/templates/
static/assets/css/style.css
media/                     uploads, gitignored
```

Drop this folder in as `Django_Projects/HMS/` on GitHub. `proj_1/` is no longer a separate app.

---

## Notes I actually hit

- Patient delete used to be a GET link. It is a confirm page + POST.
- Nurse cards used `profile_picture.url` with no check — missing photos 500. Photo is optional.
- `SECRET_KEY` is env / a **dev-only** fallback.
- 6 tests: login wall, add patient, filter, add nurse, delete POST, dashboard.

---

## License

MIT. Bootstrap stays on the CDN.
