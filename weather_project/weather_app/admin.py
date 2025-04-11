from django.contrib import admin
from .models import WeatherSearch

# Register your models here.


@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ["city", "temperature", "searched_at"]
    list_filter = ["city"]
    search_fields = ["city"]
