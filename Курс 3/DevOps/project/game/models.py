from django.conf import settings
from django.db import models
from django.db.models import Max


class ScoreEntry(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reaction_scores')
	display_name = models.CharField(max_length=150)
	score = models.PositiveIntegerField()
	played_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-score', 'display_name']

	def __str__(self) -> str:
		return f'{self.display_name}: {self.score}'

	@classmethod
	def leaderboard(cls, limit: int = 10):
		return (
			cls.objects.values('display_name')
			.annotate(best_score=Max('score'), latest_played=Max('played_at'))
			.order_by('-best_score', 'display_name')[:limit]
		)
