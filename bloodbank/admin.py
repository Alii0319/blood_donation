from django.contrib import admin
from .models import Donor, Recipient


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'city', 'age', 'gender', 'is_available', 'last_donation_date')
    list_filter = ('blood_group', 'city', 'is_available')
    search_fields = ('name', 'city', 'blood_group')
    ordering = ('name',)
    list_per_page = 20


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group_needed', 'city', 'age', 'gender', 'is_fulfilled', 'request_date')
    list_filter = ('blood_group_needed', 'city', 'is_fulfilled')
    search_fields = ('name', 'city', 'blood_group_needed')
    ordering = ('-request_date',)
    list_per_page = 20
