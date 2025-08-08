from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from researchers.models import Researcher
from django.db.models.signals import post_save
from researchers.signals import create_researcher, save_researcher


@override_settings(DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}})
class UserCreationTests(TestCase):
    """Test user creation along with nested researcher data."""

    def setUp(self):
        # Disconnect signals to emulate environment where a Researcher is not auto-created
        post_save.disconnect(create_researcher, sender=User)
        post_save.disconnect(save_researcher, sender=User)
        self.client = APIClient()

    def tearDown(self):
        # Reconnect signals after each test
        post_save.connect(create_researcher, sender=User)
        post_save.connect(save_researcher, sender=User)

    def test_create_user_with_researcher(self):
        payload = {
            "username": "alice",
            "password": "secret123",
            "researcher": {
                "expertise": "Physics",
                "institution": "MIT",
            },
        }

        response = self.client.post("/api/users/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="alice")
        researcher = Researcher.objects.get(user=user)
        self.assertEqual(researcher.expertise, "Physics")
        self.assertEqual(researcher.institution, "MIT")
