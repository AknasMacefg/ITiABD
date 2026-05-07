from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm, ScoreSubmissionForm
from .models import ScoreEntry


GAME_TOKEN_SALT = 'reaction-rush-session'
GAME_DURATION_SECONDS = 60
MAX_TOKEN_AGE_SECONDS = 90


def home(request):
	return render(
		request,
		'game/home.html',
		{
			'leaderboard': ScoreEntry.leaderboard(limit=10),
			'site_name': settings.SITE_NAME,
			'game_duration': GAME_DURATION_SECONDS,
		},
	)


def register(request):
	if request.user.is_authenticated:
		return redirect('game:home')

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Аккаунт создан. Можно начинать игру.')
			return redirect('game:play')
	else:
		form = RegistrationForm()

	return render(request, 'registration/register.html', {'form': form})


@login_required
def play(request):
	token_payload = {
		'user_id': request.user.id,
		'issued_at': timezone.now().timestamp(),
	}
	game_token = signing.dumps(token_payload, salt=GAME_TOKEN_SALT)

	return render(
		request,
		'game/play.html',
		{
			'game_token': game_token,
			'game_duration': GAME_DURATION_SECONDS,
			'leaderboard': ScoreEntry.leaderboard(limit=10),
		},
	)


@login_required
@require_http_methods(['POST'])
def submit_score(request):
	form = ScoreSubmissionForm(request.POST)
	if not form.is_valid():
		messages.error(request, 'Не удалось сохранить результат.')
		return redirect('game:play')

	score = form.cleaned_data['score']
	game_token = form.cleaned_data['game_token']

	try:
		payload = signing.loads(game_token, salt=GAME_TOKEN_SALT, max_age=MAX_TOKEN_AGE_SECONDS)
	except signing.BadSignature:
		messages.error(request, 'Сессия игры не прошла проверку целостности.')
		return redirect('game:play')

	if payload.get('user_id') != request.user.id:
		messages.error(request, 'Попытка отправить результат от другого игрока.')
		return redirect('game:play')

	ScoreEntry.objects.create(
		user=request.user,
		display_name=request.user.username,
		score=score,
	)
	messages.success(request, f'Результат сохранён: {score} очков.')
	return redirect('game:leaderboard')


def leaderboard(request):
	return render(
		request,
		'game/leaderboard.html',
		{
			'leaderboard': ScoreEntry.leaderboard(limit=20),
			'site_name': settings.SITE_NAME,
		},
	)


def logout_view(request):
	logout(request)
	return redirect('game:home')
