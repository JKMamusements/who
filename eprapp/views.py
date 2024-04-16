####################################
########### django import s#########
from django.shortcuts import render, redirect
from django.http import HttpResponse
####################################

####################################
######## Authentications ###########
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect

####################################

####################################
############ models ################ 
from .models import HomePageContent
####################################


####################################
#############  FORMS    ############
from .forms import SignUpForm
####################################







def home(request):
    return render(request, 'index.html')



def index(request):
    # Fetch the content from the database
    try:
        home_page_content = HomePageContent.objects.first()  # Assuming only one record exists
    except HomePageContent.DoesNotExist:
        home_page_content = None

    return render(request, 'index.html', {'home_page_content': home_page_content})

@csrf_protect
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

