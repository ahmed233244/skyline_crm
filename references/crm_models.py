from django.db import models
from destinations.models import user,guide,sightseeing_type,transfer_type

# Create your models here.
class client(models.Model):
    choices1=(('0','Facebook'),('1','Instagram'),('2','Tiktok'),('3','Referral'))
    sales_person=models.ForeignKey(user,on_delete=models.CASCADE)
    number=models.CharField(max_length=60,unique=True)
    name=models.CharField(max_length=60)
    platform=models.CharField(max_length=1,choices=choices1,blank=True,null=True)
    area=models.CharField(max_length=60,blank=True,null=True)
    def __str__(self):
        return self.name+' ('+self.number+ ')'
    
class flight_ticket(models.Model):
    client=models.ForeignKey(client,on_delete=models.CASCADE)
    date=models.DateField()
    From = models.CharField(max_length=60)
    to = models.CharField(max_length=60)
    flight_number = models.CharField(max_length=100,null=True,blank=True)
    time = models.TimeField(null=True,blank=True,max_length=50)
    def __str__(self):
        return str(int(self.id)+2000)
    class Meta:
        verbose_name = "Flight Ticket"
        verbose_name_plural = "Flight Tickets"
class train_ticket(models.Model):
    client=models.ForeignKey(client,on_delete=models.CASCADE)
    date=models.DateField()
    From = models.CharField(max_length=60)
    to = models.CharField(max_length=60)
    train_number=models.CharField(max_length=100,null=True,blank=True)
    time = models.TimeField(null=True,blank=True,max_length=50)
    def __str__(self):
        return str(int(self.id)+3000)
    class Meta:
        verbose_name = "Train Ticket"
        verbose_name_plural = "Train Tickets"

class hotel(models.Model):
    client=models.ForeignKey(client,on_delete=models.CASCADE)
    From = models.DateField()
    to = models.DateField()
    city=models.CharField(max_length=60)
    hotel_name=models.CharField(max_length=100)
    single_rooms=models.IntegerField(default=0)
    double_rooms=models.IntegerField(default=0)
    twin_rooms=models.IntegerField(default=0)
    triple_rooms=models.IntegerField(default=0)
    class Meta:
        verbose_name = "Hotel Booking"
        verbose_name_plural = "Hotel Bookings"

    def __str__(self):
        return str(int(self.id)+5000)
class cruise(models.Model):
    client=models.ForeignKey(client,on_delete=models.CASCADE)
    From = models.DateField()
    to = models.DateField()
    city=models.CharField(max_length=60)
    cruise_name=models.CharField(max_length=100)
    single_cabins=models.IntegerField(default=0)
    double_cabins=models.IntegerField(default=0)
    twin_cabins=models.IntegerField(default=0)
    triple_cabins=models.IntegerField(default=0)
    def __str__(self):
        return str(int(self.id)+6000)
    class Meta:
        verbose_name = "Cruise Booking"
        verbose_name_plural = "Cruise Bookings"
class sightseeing(models.Model):
    client=models.ForeignKey(client,on_delete=models.CASCADE)
    date = models.DateField()
    city=models.CharField(max_length=60)
    sightseeing = models.ForeignKey(sightseeing_type,on_delete=models.CASCADE, related_name='sightseeing2344')
    guide = models.ForeignKey(guide, on_delete=models.SET_NULL,null=True,blank=True,related_name='guide2344')
    def __str__(self):
        return str(int(self.id)+7000)
    
class transfer(models.Model):
    client=models.ForeignKey(client,on_delete=models.CASCADE)
    date = models.DateField()
    transfer = models.ForeignKey(transfer_type,on_delete=models.CASCADE,related_name='CRM_transfer')
    city = models.CharField(max_length=60)
    driver = models.CharField(max_length=100, null=True, blank=True)
    representative = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(int(self.id)+8000)
class visa(models.Model):
    c=(('0','Accepted'),('1','Rejected'))
    client=models.ForeignKey(client,on_delete=models.CASCADE)
    From = models.DateField()
    to = models.DateField()
    country=models.CharField(max_length=60)
    status=models.CharField(choices=c,max_length=1)
    reason=models.TextField(blank=True,null=True)
    def __str__(self):
        return str(int(self.id)+9000)