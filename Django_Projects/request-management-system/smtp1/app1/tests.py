from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ServiceRequest


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class RequestManagerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", "alice@example.com", "secret-pass-1")
        self.admin = User.objects.create_user(
            "boss", "boss@example.com", "secret-pass-1", is_staff=True, is_superuser=True
        )

    def test_login_required_for_form(self):
        response = self.client.get(reverse("request_form"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("next=/request/", response["Location"])

    def test_regular_user_cannot_open_admin_panel(self):
        self.client.login(username="alice", password="secret-pass-1")
        response = self.client.get(reverse("adminpanel"))
        self.assertIn(response.status_code, (302, 403))

    def test_submit_request_is_pending_and_owned(self):
        self.client.login(username="alice", password="secret-pass-1")
        self.client.post(
            reverse("request_form"),
            {
                "name": "Alice",
                "phone": "9990001111",
                "email": "alice@example.com",
                "location": "Hyderabad",
                "message": "Need a laptop",
            },
        )
        req = ServiceRequest.objects.get()
        self.assertEqual(req.submitted_by, self.user)
        self.assertEqual(req.status, ServiceRequest.PENDING)

    def test_user_cannot_approve(self):
        req = ServiceRequest.objects.create(
            submitted_by=self.user,
            name="Alice",
            phone="1",
            email="alice@example.com",
            location="x",
            message="y",
        )
        self.client.login(username="alice", password="secret-pass-1")
        response = self.client.post(reverse("approved", args=[req.id]))
        self.assertIn(response.status_code, (302, 403))
        req.refresh_from_db()
        self.assertEqual(req.status, ServiceRequest.PENDING)

    def test_staff_approve_sends_mail_and_sets_status(self):
        req = ServiceRequest.objects.create(
            submitted_by=self.user,
            name="Alice",
            phone="1",
            email="alice@example.com",
            location="x",
            message="y",
        )
        self.client.login(username="boss", password="secret-pass-1")
        self.client.post(reverse("approved", args=[req.id]))
        req.refresh_from_db()
        self.assertEqual(req.status, ServiceRequest.APPROVED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("approved", mail.outbox[0].subject.lower())
