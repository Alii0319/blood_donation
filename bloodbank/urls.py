from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register_donor/', views.register_donor, name='register_donor'),
    path('find/', views.find_donors, name='find_donors'),
    path('donor_success/',views.donor_success_view,name='donor_success'),
    path('login/',views.Login_view,name='login'),
    path('register/',views.userRegister_view,name='register'),
    path('logout/',views.logout_view,name='logout')
]
