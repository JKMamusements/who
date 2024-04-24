from django.contrib import admin
from .models import HomePageContent, Profile, Tickets, UserTicketTotal

admin.site.register(HomePageContent)
admin.site.register(Profile)
admin.site.register(Tickets)
admin.site.register(UserTicketTotal)