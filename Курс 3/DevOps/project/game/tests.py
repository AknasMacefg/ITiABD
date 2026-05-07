from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ScoreEntry


class LeaderboardTests(TestCase):
	def setUp(self):
		user = User.objects.create_user(username='alex', password='testpass123')
		ScoreEntry.objects.create(user=user, display_name='alex', score=12)

	def test_home_page_loads(self):
		response = self.client.get(reverse('game:home'))
		self.assertEqual(response.status_code, 200)

	def test_leaderboard_returns_entries(self):
		response = self.client.get(reverse('game:leaderboard'))
		self.assertContains(response, 'alex')
