from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Create your models here.
regions = (
    ('Araria','Araria'),
    ('Arwal','Arwal'),
    ('Aurangabad','Aurangabad'),
    ('Banka','Banka'),
    ('Begusarai','Begusarai'),
    ('Bhagalpur','Bhagalpur'),
    ('Bhojpur','Bhojpur'),
    ('Buxar','Buxar'),
    ('Darbhanga','Darbhanga'),
    ('East_champaran','East_Champaran'),
    ('Gaya','Gaya'),
    ('Gopalganj','Gopalganj'),
    ('Jamui','Jamui'),
    ('Jehanabad','Jehanabad'),
    ('Khagaria','Khagaria'),
    ('Kishanganj','Kishanganj'),
    ('Kaimur','Kaimur'),
    ('Katihar','Katihar'),
    ('Lakshisarai','Lakshisarai'),
    ('Madhubani','Madhubani'),
    ('Munger','Munger'),
    ('Madhepura','Madhepura'),
    ('Muzaffarpur','Muzaffarpur'),
    ('Nalanda','Nalanda'),
    ('Nawada','Nawada'),
    ('Patna','Patna'),
    ('Purnia','Purnia'),
    ('Rohtas','Rohtas'),
    ('Saharsa','Saharsa'),
    ('Samastipur','Samastipur'),
    ('Sheohar','Sheohar'),
    ('Sheikhpura','Sheikhpura'),
    ('Saran','Saran'),
    ('Sitamarhi','Sitamarhi'),
    ('Supaul','Supaul'),
    ('Siwan','Siwan'),
    ('Vaishali','Vaishali'),
    ('West_champaran','West_Champaran'),
    )

crop_types = (
    ('Kharif','Kharif'),
    ('Rabi','Rabi'),
)

seed_types = (
    ('Hybrid','Hybrid'),
    ('Local','Local'),
)

months = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    )

yesno = (
    ('Yes','Yes'),
    ('No','No'),
    )

years = (
    ('2019','2019'),
    ('2020','2020'),
    )

status = (
    ('Approved','Approved'),
    ('Notapproved','Notapproved'),
)

class registrationdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=200, choices=regions, blank=False)
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200)
    aadhar = models.BigIntegerField()
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=320, blank=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'FARMER DATA'
    
class crop_farmer(models.Model):
    email = models.EmailField(max_length=320, blank=False)
    region = models.CharField(max_length=200, choices=regions, blank=False)
    crop_type = models.CharField(max_length=200, choices=crop_types, blank=False)
    crop_name = models.CharField(max_length=200, blank=False)
    seed_type = models.CharField(max_length=200, choices=seed_types, blank=False)
    crop_year = models.CharField(max_length=200, choices=years, blank=False)
    area = models.BigIntegerField()
    days = models.BigIntegerField()
    irrigation = models.FloatField()
    fertilizers = models.BigIntegerField()
    pesticides = models.BigIntegerField()
    avg_temp = models.FloatField()
    cost = models.FloatField()
    msp = models.FloatField()
    production = models.BigIntegerField()
    approval_status = models.CharField(max_length=200, choices=status, blank=False)

    def __str__(self):
        return self.region

    class Meta:
        verbose_name_plural = 'FARMER CROP DATA'

class farm_science_expert(models.Model):
    region = models.CharField(max_length=200, choices=regions, blank=False)
    area = models.FloatField()
    crop_type = models.CharField(max_length=200, choices=crop_types, blank=False)
    crop_name = models.CharField(max_length=200, blank=False)
    seed_type = models.CharField(max_length=200, choices=seed_types, blank=False)
    days = models.BigIntegerField()
    irrigation = models.FloatField()
    fertilizers = models.BigIntegerField()
    pesticides = models.BigIntegerField()
    cost = models.FloatField()
    production = models.FloatField()

    def __str__(self):
        return self.region

    class Meta:
        verbose_name_plural = 'FARM SCIENTIST CROP DATA'

class machine_learning(models.Model):
    region = models.CharField(max_length=200, choices=regions, blank=False)
    crop_type = models.CharField(max_length=200, choices=crop_types, blank=False)
    crop_name = models.CharField(max_length=200, blank=False)
    crop_year = models.CharField(max_length=200, choices=years, blank=False)
    month = models.CharField(max_length=200, choices=months, blank=False)
    area = models.FloatField()
    avg_temp = models.FloatField()
    pressure =  models.FloatField()
    humidity = models.BigIntegerField()
    production = models.FloatField()

    def __str__(self):
        return self.region

    class Meta:
        verbose_name_plural = 'ML DATA'
    
class feedback_model(models.Model):
    first_name = models.CharField(max_length=200, blank=False)
    aadhar = models.BigIntegerField()
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=320, blank=False)
    feedback = models.CharField(max_length=2000, blank=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'FEEDBACKS'

class contacts(models.Model):
    serial_no = models.BigIntegerField()
    name = models.CharField(max_length=200, blank=False)
    designation = models.CharField(max_length=200, blank=False)
    mobile = models.BigIntegerField()
    email = models.EmailField(max_length=320, blank=False)
    address = models.CharField(max_length=500, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'CONTACTS'
