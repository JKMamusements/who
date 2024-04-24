from django.db import models
from django.contrib.auth.models import User


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
    num_tickets_genrated = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)

class UserTicketTotal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_tickets_genrated = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)


