from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class ScoreSubmissionForm(forms.Form):
    score = forms.IntegerField(min_value=0)
    game_token = forms.CharField()