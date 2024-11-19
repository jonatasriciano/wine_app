from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class WinePreference(models.Model):
    """
    Model to store user wine preferences.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wine_type = models.CharField(max_length=20)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    grape_region = models.ManyToManyField('GrapeRegion', related_name='preferences')
    sensory_perception = models.JSONField()
    social_psychological = models.TextField()
    selection_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s preference for {self.wine_type}"


class WineRecommendation(models.Model):
    """
    Model to store wine recommendations for each wine preference.
    """
    preference = models.ForeignKey(WinePreference, on_delete=models.CASCADE, related_name="recommendations")
    wine_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    grape_variety = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    # Step 1: `created_at` with null=True for existing data compatibility
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    link = models.URLField(max_length=255, blank=True)
    def __str__(self):
        return f"Recommendation: {self.wine_name} for {self.preference.selection_name}"


class GrapeRegion(models.Model):
    """
    Model to store grape regions with specific details.
    """
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
    famous_for = models.CharField(max_length=255)
    availability = models.CharField(max_length=50)
    country_code = models.CharField(max_length=5, blank=True, help_text="ISO 3166-1 alpha-2 country code")

    class Meta:
        ordering = ['name']  # Sort regions alphabetically by name

    def __str__(self):
        return f"{self.name} - {self.country}"