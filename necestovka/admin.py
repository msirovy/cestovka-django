from django.contrib import admin

from .models import Users, Flights, Orders
from django.forms import TextInput, Textarea
from django.db import models

class UsersInline(admin.TabularInline):
    model = Users
    extra = 0   # pocet predvytvorenych
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':15})},
    }

class FlightsInline(admin.StackedInline):
    list_filter = ('fly_no', 'start_place', 'arrive_place')
    classes = ('grp-collapse grp-open',)
    model = Flights
    '''fieldsets = (
        (None, {
            'classes': ('grp-collapse grp-open',),
            'fields' : ('fly_no','airlines')
        }),
        ('Detail', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('start_place', 'start_time'),('arrive_place', 'arrive_time'))
        }),
    )'''
    fields = (
        ('fly_no','airlines'),
        ('start_place', 'start_time'),
        ('arrive_place', 'arrive_time')
    )
    extra = 0   # pocet predvytvorenych

class OrdersAdmin(admin.ModelAdmin):
    view_on_site = False
    save_as = True
    readonly_fields = ['order_date']
    fieldsets = (
        ("Objednavka", {
            'fields': ('id', 'order_date', 'state', 'price')
        }),
        ("Kontakt:", {
            'description': 'Vyplnte kontakt na zakaznika, ktery provedl objednavku',
            'fields': ('contact_name', 'contact_email', 'contact_phone')
        })
    )
    inlines = [
        UsersInline,
        FlightsInline
    ]


admin.site.register(Users)
admin.site.register(Flights)
admin.site.register(Orders, OrdersAdmin)