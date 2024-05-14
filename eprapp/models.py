from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class HomePageContent(models.Model):
    content = models.TextField()

    def __str__(self):
        return f"Home Page Content ({self.pk})"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username    


class Tickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_tickets_generated = models.IntegerField()
    generated_at = models.TimeField(default=timezone.now)  # Store the time in UTC by default
    generated_date = models.DateField(default=date.today) 

class UserTicketTotal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_tickets_generated = models.IntegerField(default=0)
    date = models.DateField(default=date.today)  # Store the date in UTC by default
    class Meta:
        unique_together = ('user', 'date')