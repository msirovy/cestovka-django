from django.db import models
from random import randrange
from datetime import datetime


def auto_id():
    return str(datetime.now().strftime("%m%y")) + str(randrange(9999))

class Airports(models.Model):
    class Meta:
        verbose_name_plural = 'Letiště'

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)


class Airlines(models.Model):
    class Meta:
        verbose_name_plural = 'Aerolinky'
        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Flights(models.Model):
    class Meta:
        verbose_name_plural = 'Lety'
    
    id = models.AutoField(primary_key=True)
    start_place = models.ForeignKey('Airports', 
                                    related_name='fk_start_airport')
    start_time = models.DateTimeField()
    arrive_place = models.ForeignKey('Airports',
                                    related_name='fk_arrive_airport')
    arrive_time = models.DateTimeField()
    airlines = models.ForeignKey('Airlines',
                                related_name='fk_fly_airlines')
    orders = models.ForeignKey('Orders',
                            related_name='fk_fly_orders')

    def __str__(self):
        return "{} -> {} ({})".format(self.start_place, self.arrive_place, self.airlines)


class Tickets(models.Model):
    class Meta:
        verbose_name_plural = 'Letenky'

    id = models.AutoField(primary_key=True)
    booking_ref = models.CharField(max_length=15)
    booking_status = models.CharField(max_length=50, default="")
    fly_number = models.CharField(max_length=30, blank=True)
    depart_place = models.ForeignKey('Airports', 
                                    related_name='fk_ticket_depart_airport')
    depart_time = models.DateTimeField()
    arrive_place = models.ForeignKey('Airports',
                                    related_name='fk_ticket_arrive_airport')
    arrive_time = models.DateTimeField()
    airlines = models.ForeignKey('Airlines',
                                related_name='fk_ticket_airlines', blank=True)
    terminal = models.CharField(max_length=15, blank=True)
    baggage_allowed = models.CharField(max_length=200, blank=True)
    passenger = models.ForeignKey('Passengers',
                            related_name='fk_ticket_passenger')
    orders = models.ForeignKey('Orders',
                            related_name='fk_ticket_orders', blank=True)
    #ticket_pdf = 

    def __str__(self):
        return "{} ({} -> {})".format(self.booking_ref, self.depart_place, self.arrive_place)


class Extras(models.Model):
    class Meta:
        verbose_name_plural = 'Volitelné služby'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    #orders = models.ForeignKey('Orders', related_name='fk_extras_orders')

    def __str__(self):
        return self.name


class Orders(models.Model):
    ''' Objednavky
    '''
    class Meta:
        verbose_name_plural = 'Objednávky'
    
    STATE = (
        ('paid','Zaplacena'),
        ('in_progress', 'Rozpracovana'),
        ('new', 'Nova'),
        ('canceled', 'Zrusena')
    )
    BANKS = (
        ('CSOB','CSOB'), 
        ('Unicredit','Unicredit'), 
        ('KB','KB')
    )
    id = models.CharField(primary_key=True, default=auto_id, max_length=8)
    order_date = models.DateTimeField(auto_now_add=True)
    final_price = models.IntegerField(blank=True, null=True)
    contact_name = models.ForeignKey('Passengers', related_name='fk_orders_passenger_primary')
    passangers_count = models.IntegerField(blank=True, null=True)
    checked_luggage = models.IntegerField(blank=True, null=True)
    state = models.CharField(choices=STATE, max_length=50)
    bank_name = models.CharField(choices=BANKS, max_length=50, blank=True)
    extras = models.ForeignKey('Extras', related_name='fk_orders_extras', blank=True, null=True)
    ordered_flights = models.ForeignKey('Flights', related_name='fk_orders_ordered_flights', blank=True, null=True)
    passengers = models.ForeignKey('Passengers', related_name='fk_orders_passengers', blank=True, null=True)

    def __str__(self):
        return "{} - {} ({})".format(self.id, self.order_date, self.contact_name)

    @property
    def price_per_person(self):
        ''' return price per person by math
        '''
        return 0

    @property
    def create_new(self):
        '''
        	order_create(
		fly={
			1:{
				"from":
				"to":
				"start_date":
				"return_date":
			}
		},
		primary_email="",
		primary_phone="",
		passangers=int(),
		checked_luggage=int()
        '''
        pass


class Passengers(models.Model):
    class Meta:
        verbose_name_plural = 'Pasažéři'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    born_date = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    luggage_hand = models.CharField(max_length=25, blank=True, null=True)
    luggage_cabin = models.CharField(max_length=25, blank=True, null=True)
    luggage_checked = models.CharField(max_length=25, blank=True, null=True)
    tickets = models.ForeignKey('Tickets',
                                related_name='fk_passengers_tickets', blank=True, null=True)
    orders = models.ForeignKey('Orders',
                                related_name='fk_passengers_orders', blank=True, null=True)
    
    def __str__(self):
        return "{} ({} {})".format(self.name, self.email, self.phone)

    def add_flight(self):
        pass
