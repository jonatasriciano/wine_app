# preferences/models.py

from django.db import models
from django.contrib.auth.models import User

class WinePreference(models.Model):
    """
    Model to store user wine preferences.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate preferences with the user
    wine_type = models.CharField(max_length=20)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    grape_region = models.ManyToManyField('GrapeRegion', related_name='preferences')  # Many-to-many relationship with GrapeRegion
    sensory_perception = models.JSONField()
    social_psychological = models.TextField()
    selection_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s preference for {self.wine_type}"

class WineRecommendation(models.Model):
    """
    Model to store wine recommendations for each preference.
    """
    preference = models.ForeignKey(WinePreference, on_delete=models.CASCADE, related_name="recommendations")
    wine_name = models.CharField(max_length=100)  # Name of the recommended wine
    region = models.CharField(max_length=100)  # Region of the wine
    grape_variety = models.CharField(max_length=100)  # Grape variety of the wine
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the wine
    description = models.TextField()  # Description or notes about the wine

    def __str__(self):
        return f"Recommendation: {self.wine_name} for {self.preference.selection_name}"
    
class GrapeRegion(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
    famous_for = models.CharField(max_length=255)
    availability = models.CharField(max_length=50)
    country_code = models.CharField(max_length=5, help_text="Country code", blank=True)

    class Meta:
        ordering = ['name']  # Order alphabetically by name

    def __str__(self):
        return f"{self.name} - {self.country}"