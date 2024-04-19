####################################
########### django import s#########
from django.shortcuts import render, redirect
from django.http import HttpResponse
####################################
from django.contrib import messages
####################################
######## Authentications ###########
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

####################################

####################################
############ models ################ 
from .models import HomePageContent, Profile
####################################


####################################
#############  FORMS    ############
from .forms import SignUpForm, ProfileForm
####################################

def home(request):
    return render(request, 'index.html')

def index(request):
    # Fetch the content from the database
    home_page_content = HomePageContent.objects.first()  # Returns None if no entry exists

    return render(request, 'index.html', {'home_page_content': home_page_content})

@csrf_protect
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile for the user
            Profile.objects.create(user=user)
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
        messages.error(request, "Invalid username or password.")  # Moved error message outside of the 'is_valid' block
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('signin')



from django.contrib import messages
from django.shortcuts import redirect

def user_dashboard(request):
    if request.user.is_anonymous:
        #messages.error(request, "Please sign in first.")
        return redirect('signin')

    # Default full name is 'Guest'
    full_name = "Guest"

    # Obtain username from the user object
    username = request.user.get_username()

    # Construct full name using first name and last name from the User model
    try:
        profile = request.user.profile
        # Construct full name using first name and last name from the Profile model
        full_name = f"{profile.first_name} {profile.last_name}".strip()
    except Profile.DoesNotExist:
        pass  # Keep the default full name if no profile exists

    return render(request, "user_dashboard.html", {'username': username, 'full_name': full_name})


def update_profile(request):
    if request.user.is_anonymous:
        return redirect('signin')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form})


            

