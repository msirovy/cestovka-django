from django.contrib import admin

from .models import Passengers, Flights, Orders, Airports, Airlines, Extras, Tickets
from django.forms import TextInput, Textarea
from django.db import models
from django.utils.safestring import mark_safe
from docxtpl import DocxTemplate
from django.conf import settings
from django.http import HttpResponse
from io import BytesIO
import os
from shutil import make_archive
import random
from time import sleep

def export_as_docx(modeladmin, request, queryset):
    try:
        work_id = 'req-{}'.format(random.randrange(99999))
        work_dir = os.path.join(settings.TMP_DIR, work_id)
        for item in queryset:
            order_id=str(item.id)
            os.makedirs(os.path.join(work_dir, order_id))
            
            f = []
            for fly in item.fk_fly_orders.all():
                f.append({
                    "start": fly.start_place.__str__(),
                    "start_time": fly.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "arrive": fly.arrive_place.__str__(),
                    "arrive_time": fly.arrive_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "airlines": fly.airlines.name,
                    "fly_id": fly.fly_no,
                    "cabin": fly.cabin_lugg,
                    "checked_lugg": fly.checked_lugg
                })
            for user in item.fk_users_orders.all():
                print("Working on user %s" % user.name)
                x_tpl = DocxTemplate(settings.EXPORT_TPL['order'])
                data = {
                    "client_name": user.name,
                    "order_id": order_id,
                    "flights": f
                }
                file_name = os.path.join(work_dir, order_id, '{order_id}-{client_name}.docx'.format_map(data))
                # generate file in memmory and download them
                fs = BytesIO()
                x_tpl.render(data)
                x_tpl.save(file_name)

        # zip files and download them
        zip_path = os.path.join(settings.TMP_DIR, "{}.zip".format(work_id))
        print(zip_path)
        make_archive("{}{}".format(settings.TMP_DIR, work_id), 'zip', work_dir)
        response = HttpResponse(open(zip_path, 'rb'), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename={}.zip'.format(work_id)
        print("get file")
        return response

    except IOError as err:
        print(err)
    #yield "file"
export_as_docx.short_description = "Export as DOCX"


class NecestovkaAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/admin.css',)
        }


class PassengersInline(admin.TabularInline):
    model = Passengers
    extra = 0   # pocet predvytvorenych
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':15})},
    }


class TicketsInline(admin.StackedInline):
    list_filter = ('booking_ref', 'start_place', 'arrive_place', 'airlines', 'start_time')
    list_filter = ('booking_ref', 'start_place', 'arrive_place', 'airlines', 'start_time')
    classes = ('grp-collapse grp-open',)
    model = Tickets
    fields = (
        ('booking_ref', 'passenger'),
        ('airlines', 'terminal'),
        ('depart_place', 'depart_time'),
        ('arrive_place', 'arrive_time'),
        ('baggage_allowed')
    )
    extra = 0


class FlightsInline(admin.StackedInline):
    list_filter = ('start_place', 'arrive_place', 'airlines', 'start_time')
    list_filter = ('start_place', 'arrive_place', 'airlines', 'start_time')
    classes = ('grp-collapse grp-open',)
    model = Flights
    fields = (
        ('airlines'),
        ('start_place', 'start_time'),
        ('arrive_place', 'arrive_time'),
    )
    extra = 0   # pocet predvytvorenych

class OrdersAdmin(NecestovkaAdmin):
    search_fields = ('id', 'contact_name__name', 'state', 'order_date')
    list_display = ('id', 'contact_name', 'final_price', 'state', 'order_date', 'exportAsDocx')
    view_on_site = False
    save_as = True
    readonly_fields = ['order_date']
    fieldsets = (
        ("Objednavka", {
            'fields': (
                'id', 
                'order_date', 
                'contact_name', 
                'state', 
                'final_price',
                'checked_luggage'
                )
        }),
    )
    inlines = [
        TicketsInline,
        FlightsInline
    ]
    actions = [export_as_docx]

    def exportAsDocx(self, obj):
        return mark_safe("<button name='docx' value='save as docx'>DOCX</button> <button name='docx' value='save as docx'>PDF</button>")
    exportAsDocx.short_description = "Export"


class PassengersAdmin(NecestovkaAdmin):
    inlines = [
        TicketsInline
    ]


admin.site.register(Airports)
admin.site.register(Airlines)
admin.site.register(Passengers, PassengersAdmin)
admin.site.register(Flights)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Extras)
admin.site.register(Tickets)