from django.db import models

# Create your models here.


class WeatherSearch(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C @ {self.searched_at.strftime('%Y-%m-%d %H:%M:%S')}"
