from django.db import models

class HomePageContent(models.Model):
    content = models.TextField()

    def __str__(self):
        return f"Home Page Content ({self.pk})"
