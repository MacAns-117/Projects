from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Nurse, Patient


class HospitalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", "a@example.com", "secret-pass-1")

    def test_login_required(self):
        response = self.client.get(reverse("patient_list"))
        self.assertEqual(response.status_code, 302)

    def test_add_patient(self):
        self.client.login(username="alice", password="secret-pass-1")
        self.client.post(
            reverse("patient_create"),
            {
                "name": "Ravi",
                "blood_group": "O+",
                "age": 34,
                "disease": "Fever",
                "location": "Hyderabad",
            },
        )
        self.assertEqual(Patient.objects.get().name, "Ravi")

    def test_filter_patient_by_name(self):
        Patient.objects.create(name="Ravi", blood_group="O+", age=34, disease="Fever", location="Hyd")
        Patient.objects.create(name="Meera", blood_group="A+", age=22, disease="Cold", location="Hyd")
        self.client.login(username="alice", password="secret-pass-1")
        response = self.client.get(reverse("patient_list"), {"q": "Ravi"})
        self.assertContains(response, "Ravi")
        self.assertNotContains(response, "Meera")

    def test_add_nurse(self):
        self.client.login(username="alice", password="secret-pass-1")
        self.client.post(
            reverse("nurse_create"),
            {
                "name": "Priya",
                "gender": "F",
                "department": "Cardiology",
                "shift": "5:00 AM - 1:00 PM",
                "care": "ICU",
                "experience": 4,
                "certifications": "BLS",
                "contact_number": "9990001111",
                "email": "priya@example.com",
                "address": "Ward 2",
            },
        )
        self.assertEqual(Nurse.objects.get().name, "Priya")

    def test_delete_patient_post(self):
        p = Patient.objects.create(name="Ravi", blood_group="O+", age=34, disease="Fever", location="Hyd")
        self.client.login(username="alice", password="secret-pass-1")
        self.client.post(reverse("patient_delete", args=[p.pk]))
        self.assertFalse(Patient.objects.filter(pk=p.pk).exists())

    def test_dashboard_counts(self):
        Patient.objects.create(name="Ravi", blood_group="O+", age=34, disease="Fever", location="Hyd")
        self.client.login(username="alice", password="secret-pass-1")
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "1")
