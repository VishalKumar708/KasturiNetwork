from typing import Any
from django.contrib import admin

from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from .models import *

class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'state_name', 'isActive', 'createdBy', 'updatedBy', 'formatted_created_date', 'formatted_updated_date']

    # remove not required field 
    exclude = ('createdBy', 'updatedBy')

    # automatic save createdBy and updatedBy
    def save_model(self, request, obj, form, change):
        # Set createdBy and updatedBy fields based on the logged-in user
        if not obj.pk:  # Only for new instances
            obj.createdBy = request.user
        obj.updatedBy = request.user
        super().save_model(request, obj, form, change)

    def formatted_created_date(self, obj):
        return obj.createdDate.strftime('%d %B, %Y %I:%M %p')

    def formatted_updated_date(self, obj):
        return obj.updatedDate.strftime('%d %B, %Y %I:%M %p')
    
    formatted_created_date.short_description = 'Created Date'
    formatted_updated_date.short_description = 'Updated Date'

admin.site.register(State, StateAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'country_name', 'isActive', 'createdBy', 'updatedBy', 'formatted_created_date', 'formatted_updated_date']
    # remove not required field 
    exclude = ('createdBy', 'updatedBy')

    # automatic save createdBy and updatedBy
    def save_model(self, request, obj, form, change):
        # Set createdBy and updatedBy fields based on the logged-in user
        if not obj.pk:  # Only for new instances
            obj.createdBy = request.user
        obj.updatedBy = request.user
        super().save_model(request, obj, form, change)

    def formatted_created_date(self, obj):
        return obj.createdDate.strftime('%d %B, %Y %I:%M %p')

    def formatted_updated_date(self, obj):
        return obj.updatedDate.strftime('%d %B, %Y %I:%M %p')
    
    formatted_created_date.short_description = 'Created Date'
    formatted_updated_date.short_description = 'Updated Date'

admin.site.register(Country, CountryAdmin)



class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'state_name', 'city_name', 'isActive', 'createdBy', 'updatedBy', 'formatted_created_date', 'formatted_updated_date']
    # remove not required field 
    exclude = ('createdBy', 'updatedBy')

    # automatic save createdBy and updatedBy
    def save_model(self, request, obj, form, change):
        # Set createdBy and updatedBy fields based on the logged-in user
        if not obj.pk:  # Only for new instances
            obj.createdBy = request.user
        obj.updatedBy = request.user
        super().save_model(request, obj, form, change)

    def formatted_created_date(self, obj):
        return obj.createdDate.strftime('%d %B, %Y %I:%M %p')

    def formatted_updated_date(self, obj):
        return obj.updatedDate.strftime('%d %B, %Y %I:%M %p')
    
    formatted_created_date.short_description = 'Created Date'
    formatted_updated_date.short_description = 'Updated Date'

admin.site.register(City, CityAdmin)
# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'mobile_number', 'telephone', 'mail_id', 
                    'country', 'state', 'city', 'district', 'address', 'pin_code', 'service_type',
                    'account_holder_name', 'account_number', 'bank_name', 'ifsc_code', 'branch_name', 'pan_number', 'gst_number', 'payment_terms',
                    'name', 'phone_number',
                    'address_proof', 'company_proof', 'cancelled_check', 'gst_in', 'pan_card', 'attachment1', 'agreement', 'tds_excemption_certificate']
    
    #show field categry wise when user add any record in this model
    fieldsets = [
        ('Company Details', {'fields': ['company_name', 'owner', 'mobile_number', 'telephone', 'mail_id']}),
        ('Address Details', {'fields': ['country', 'state', 'city', 'district', 'address', 'pin_code', 'service_type']}),
        ('Bank Details', {'fields': ['account_holder_name', 'account_number', 'bank_name', 'ifsc_code', 'branch_name', 'pan_number', 'gst_number', 'payment_terms']}),
        # Add more fieldsets as needed
        ('Contact Details', {'fields': ['name', 'phone_number']}),
        ('Documents', {'fields': ['address_proof', 'company_proof', 'cancelled_check', 'gst_in', 'pan_card', 'attachment1', 'agreement', 'tds_excemption_certificate']}),
    ]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs['queryset'] = Country.objects.filter(isActive=True)
        if db_field.name == 'state':
            kwargs['queryset'] = State.objects.filter(isActive=True)
        if db_field.name == "city":
            kwargs['queryset'] = City.objects.filter(isActive=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('customjs/my_file.js',)
        

admin.site.register(Client, ClientAdmin)


