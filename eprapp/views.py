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
from .models import HomePageContent, Profile, Tickets, UserTicketTotal
####################################


####################################
#############  FORMS    ############
from .forms import SignUpForm, ProfileForm
####################################

####################################
#############  FORMS    ############
from .utils import create_tickets, generate_single_pass
####################################

import os
from PIL import Image
from datetime import date, datetime


from django.utils import timezone



def home(request):
    return render(request, 'index.html')


def Blogs(request):
    return render(request, 'Blogs.html')

def index(request):
    # Fetch the content from the database
    return render(request, 'index.html', {})

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

QR_CODE_DIR = 'static/tickets/'            
TICKET_TEMPLATE_DIR = TICKET_TEMPLATE_DIR = "static/ticket_info/ticket_template.png"
FONT_PATH = "static/ticket_info/Roboto-Medium.ttf"


def counter(request):
    
    if request.user.is_anonymous:
        return redirect('signin')
    
    username = request.user.get_username()
    
    if request.method == "POST":
        num = int(request.POST.get('display', 0))
        
        if num == 0:
            return render(request, "counter.html", {'csrf_token': request.POST.get('csrfmiddlewaretoken')})
        
        # Retrieve total tickets count for the user
        user_ticket_total, created = UserTicketTotal.objects.get_or_create(
            user=request.user,
        )
        total_tickets = user_ticket_total.total_tickets_generated
        
        date_now = datetime.now()
        time_now = datetime.now().time()
        
        info = {
            "username": username,
            "date": date_now,
            "time": time_now,
            "total_tickets": total_tickets,
            "tickets_in_pass": num,
            "location": "Ghaziabad",
            "price": "100"  # This can be modified as needed
        }
        
        # Define text info dictionary
        text_info = {
            f"{info['date'].strftime('%d-%m-%Y')}": (410, 550),
            f"{info['time'].strftime('%H:%M:%S')}": (410, 630),
            f"{info['location']}": (410, 780),
            f"{info['price']}": (410, 700),
            f"Tickets in this pass: {info['tickets_in_pass']}": (210, 480)
        }
        
        os.makedirs(QR_CODE_DIR, exist_ok=True)
        
        ticket_template = Image.open(TICKET_TEMPLATE_DIR)
        pass_image = generate_single_pass(info, text_info, ticket_template, font_path=FONT_PATH)

        # Save the image with the username as part of the filename
        image_filename = f"{username}.png"
        image_path = os.path.join(QR_CODE_DIR, image_filename)
        pass_image.save(image_path)
        
        # Create Tickets instances
        Tickets.objects.create(user=request.user, num_tickets_generated=num, generated_at=timezone.now())
        
        # Update UserTicketTotal instance
        user_ticket_total.total_tickets_generated += num
        user_ticket_total.save()

        return redirect('counter')

    # Retrieve total tickets count for the user
    user_ticket_total, created = UserTicketTotal.objects.get_or_create(user=request.user)
    total_count = user_ticket_total.total_tickets_generated
    
    info = {"username": username, "total_tickets": total_count}
    return render(request, "counter.html", info)


def counter2(request):
    if request.user.is_anonymous:
        return redirect('signin')
    
    username = request.user.get_username()
    
    if request.method == "POST":
        num = int(request.POST.get('display', 0))
        
        if num == 0:
            # Include the CSRF token when rendering the template
            return render(request, "counter.html", {'csrf_token': request.POST.get('csrfmiddlewaretoken')})
        
        # Retrieve total tickets count for the user
        user_ticket_total, created = UserTicketTotal.objects.get_or_create(user=request.user)
        start_number = user_ticket_total.total_tickets_generated
        margin = 20
        os.makedirs(QR_CODE_DIR, exist_ok=True)
        
        ticket_template = Image.open(TICKET_TEMPLATE_DIR)       
        canvas = create_tickets(num, start_number, ticket_template, margin=margin, data_prefix="JKM2024", font_path=FONT_PATH)

        # Save the image with the username as part of the filename
        image_filename = f"{username}.png"
        image_path = os.path.join(QR_CODE_DIR, image_filename)
        canvas.save(image_path)
        
        # Create Tickets instances
        Tickets.objects.create(user=request.user, num_tickets_generated=num, generated_at=timezone.now())
        
        # Update UserTicketTotal instance
        user_ticket_total.total_tickets_generated += num
        user_ticket_total.save()

        return redirect('counter')

    # Retrieve total tickets count for the user
    user_ticket_total, created = UserTicketTotal.objects.get_or_create(user=request.user)
    total_count = user_ticket_total.total_tickets_generated
    
    info = {"username": username, "total_tickets": total_count}
    return render(request, "counter.html", info)





from django.db.models import Sum
from django.db import connection

def view_tickets(request):
    today = date.today()

    user_ticket_totals = UserTicketTotal.objects.all()
    return render(request, 'tickets.html', {'user_ticket_totals': user_ticket_totals,  })



