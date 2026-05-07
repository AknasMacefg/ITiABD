from django.contrib import admin

from .models import ScoreEntry


@admin.register(ScoreEntry)
class ScoreEntryAdmin(admin.ModelAdmin):
	list_display = ('display_name', 'score', 'played_at')
	search_fields = ('display_name', 'user__username')
	list_filter = ('played_at',)
