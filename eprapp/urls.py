from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.update_profile, name='update_profile'),
    path('signin/', views.signin, name='signin'),  # Assuming you have a custom login view
    path('signout/', views.signout, name='signout'),
    path("counter/", views.counter , name="counter"),
    path("Blogs/", views.Blogs , name="Blogs"),
    path("tickets/", views.view_tickets , name="tickets")
]   
