<h1>Django Projects</h1>

<p>
  <img src="https://img.shields.io/badge/projects-3-blue?style=flat-square" alt="3 projects">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.0-092E20?style=flat-square&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

> Three Django apps — login and CRUD on SQLite on every one, Bootstrap 5 on the pages, console mail on the request app so SMTP is optional.

---

## What's in here

| Folder | What it is | Headline |
| --- | --- | --- |
| [`todo`](todo/) | Task list, per user | **6** tests; Bob gets **404** on Alice’s delete |
| [`smtp1`](smtp1/) | Request form + staff approve/reject | Status is stored (`pending` → `approved` / `rejected`); **5** tests |
| [`HMS`](HMS/) | Patients **and** nurses in one app | **2** models, one dashboard, **6** tests |

Each folder has its own README with run steps and the test list. `proj_1/` is not a separate app — patients live in `HMS/` with the nurses.

---

## Task Manager — `todo`

Sign up, log in, keep a **private** list. Add / edit / delete in Bootstrap modals. Toggle Pending ↔ Completed. Filter by status on View Tasks.

| | |
| --- | --- |
| Model | `Task`: name, description, status, **owner**, created_at |
| Auth | `login_required` on every task page. `LOGIN_URL` is `login`. |
| Isolation | Home lists `request.user` only. Foreign delete is **404**. |
| Delete | POST form, not a GET link |

CRUD + auth. No reminders, no teams, no API.

---

## Request Management — `smtp1`

A user files a request. Staff open `/adminpanel/`, filter pending / approved / rejected, POST approve or reject. Mail goes out.

| Role | Can do |
| --- | --- |
| Regular user | Sign up, submit a request, see **their** rows |
| Staff (`is_staff=True`) | Panel + approve / reject |

Approve **writes a status**. Mail defaults to the **console**, so this runs without Gmail. Real SMTP is env vars (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`) — not in the repo.

`ServiceRequest`: name, phone, email, location, message, status, owner, timestamps. No SLAs, no attachments.

---

## Hospital records — `HMS`

Patient details and the nurse list are **one** project. One login, one nav, two models.

| | Patients | Nurses |
| --- | --- | --- |
| Fields | name, blood group, age, disease, location | name, gender, department, shift, care, years, certs, phone, email, optional photo |
| List | filter by id or name | filter by department / shift |
| Write | add / edit / delete (POST) | add / edit / delete (POST) |

Dashboard shows the two counts. Photo is optional — a missing file does not 500. Pillow is required because of `ImageField`. No wards, no appointments, no billing.

---

## Tech stack across all three

| Layer | Tools |
| --- | --- |
| Language | Python 3 |
| Framework | Django 5.0 |
| Database | SQLite (`db.sqlite3`, gitignored) |
| Auth | Django `User` + `login_required` |
| Forms | Django `ModelForm` / `UserCreationForm` |
| UI | Bootstrap 5 (CDN) |
| Mail (`smtp1`) | `console` backend by default; SMTP optional |
| Images (`HMS`) | Pillow + `MEDIA_ROOT` |
| Tests | Django `TestCase` — 6 / 5 / 6 |

No MySQL required. No React.

---

## How to run any of them

```bash
cd todo          # or smtp1 or HMS
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py test
```

`createsuperuser` is optional except on `smtp1`, where staff is how you reach the admin panel.

---

## Layout

```text
README.md          this file
todo/              Task Manager
smtp1/             Request Management
HMS/               Hospital records (patients + nurses)
```

Open a folder and follow that child’s README.

---

## Limits

- `SECRET_KEY` is `DJANGO_SECRET_KEY` or a **dev-only** fallback. Do not use the fallback on a public host.
- Do not commit `db.sqlite3`. Do not commit SMTP passwords.
- `smtp1` mail is console unless you set env vars. If an older copy had a Gmail app password in `settings.py`, rotate that password.
- `HMS` photos go in `media/nurse_pics/` (gitignored). Uploaded files are not in git.

---

## License

Code is MIT unless a child README says otherwise. Bootstrap / Boxicons / Font Awesome stay with their CDNs.
