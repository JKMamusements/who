from django.shortcuts import render
from django.http import HttpResponse
from .models import HomePageContent

def home(request):
    return render(request, 'index.html')



def index(request):
    # Fetch the content from the database
    try:
        home_page_content = HomePageContent.objects.first()  # Assuming only one record exists
    except HomePageContent.DoesNotExist:
        home_page_content = None

    return render(request, 'index.html', {'home_page_content': home_page_content})