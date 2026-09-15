from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskManagerTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", "alice@example.com", "secret-pass-1")
        self.bob = User.objects.create_user("bob", "bob@example.com", "secret-pass-1")
        self.alice_task = Task.objects.create(
            owner=self.alice, task_name="Alice only", description="private", status=Task.PENDING
        )
        Task.objects.create(owner=self.bob, task_name="Bob only", description="other", status=Task.PENDING)

    def test_login_required_redirects(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_user_sees_only_own_tasks(self):
        self.client.login(username="alice", password="secret-pass-1")
        response = self.client.get(reverse("index"))
        self.assertContains(response, "Alice only")
        self.assertNotContains(response, "Bob only")

    def test_add_task_sets_owner(self):
        self.client.login(username="alice", password="secret-pass-1")
        self.client.post(
            reverse("add_task"),
            {"task_name": "Buy milk", "description": "2L", "status": Task.PENDING},
        )
        task = Task.objects.get(task_name="Buy milk")
        self.assertEqual(task.owner, self.alice)

    def test_cannot_delete_someone_elses_task(self):
        self.client.login(username="bob", password="secret-pass-1")
        response = self.client.post(reverse("delete_task", args=[self.alice_task.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(id=self.alice_task.id).exists())

    def test_change_status_toggles(self):
        self.client.login(username="alice", password="secret-pass-1")
        response = self.client.post(reverse("change_status", args=[self.alice_task.id]))
        self.assertEqual(response.json()["new_status"], Task.COMPLETED)

    def test_signup_then_login(self):
        self.client.post(
            reverse("signup"),
            {
                "username": "cara",
                "email": "cara@example.com",
                "password1": "secret-pass-1",
                "password2": "secret-pass-1",
            },
        )
        logged_in = self.client.login(username="cara", password="secret-pass-1")
        self.assertTrue(logged_in)
