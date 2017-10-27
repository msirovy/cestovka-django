from django.db import models

class Flights(models.Model):
    id = models.AutoField(primary_key=True)
    start_place = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    arrive_place = models.CharField(max_length=20)
    arrive_time = models.DateTimeField()
    airlines = models.CharField(max_length=20)
    fly_no = models.CharField(max_length=10)
    orders = models.ForeignKey('Orders', related_name='fly2orders', on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({} -> {})".format(self.fly_no, self.start_place, self.arrive_place)


class Orders(models.Model):
    ''' Objednavky
    '''
    STATE = (
        ('zaplacena','Zaplacena'),
        ('rozpracovana', 'Rozpracovana'),
        ('nova', 'Nova'),
        ('zrusena', 'Zrusena')
    )
    id = models.IntegerField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    contact_name = models.CharField(max_length=25)
    contact_email = models.EmailField(max_length=25)
    contact_phone = models.CharField(max_length=12)
    state = models.CharField(choices=STATE, max_length=10)

    def __str__(self):
        return "{} - {} ({})".format(self.id, self.contact_email, self.order_date)

    @property
    def price_per_person(self):
        ''' return price per person by math
        '''
        return 0


class Users(models.Model):
    CABIN_LUGG = (
        ('1', '21x21x24'),
        ('2', '22x22x21')
    )
    CHECKED_LUGG = (
        ('1', '40x50x60'),
        ('2', '50x65x45')
    )
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    born_year = models.IntegerField()
    email = models.EmailField(max_length=30)
    cabin_lugg = models.CharField(choices=CABIN_LUGG, max_length=10)
    checked_lugg = models.CharField(choices=CHECKED_LUGG, max_length=10)
    orders = models.ForeignKey('Orders', related_name='user2orders', on_delete=models.CASCADE)

    def __str__(self):
        return self.email