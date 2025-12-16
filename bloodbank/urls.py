from django.urls import path
from . import views

urlpatterns = [
    # Home & Authentication
    path('', views.home, name='home'),
    path('login/', views.Login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.userRegister_view, name='register'),

    # Donor Management
    path('register_donor/', views.register_donor, name='register_donor'),
    path('donor_success/', views.donor_success_view, name='donor_success'),

    # Donor Requests (Donor Side)
    path('my-requests/', views.donor_requests, name='donor_requests'),
    path('update-request/<int:request_id>/<str:status>/', views.update_request_status, name='update_request'),

    # Recipient Actions
    path('find/', views.find_donors, name='find_donors'),
    path('send-request/<int:donor_id>/', views.send_request, name='send_request'),
    path('my-requests-recipient/', views.recipient_requests, name='recipient_requests'),
]
