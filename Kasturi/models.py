from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class BaseModel(models.Model):
    isActive = models.BooleanField(default=True)
    # groupId = models.CharField(max_length=40, default=1)
    createdBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_created',
        null=True, 
        blank=True
    )
    updatedBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_updated',
        null=True,
        blank=True
    )
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Country(BaseModel):
    id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=30, unique = True)

    def save(self, *args, **kwargs):
        self.state_name = self.country_name.capitalize()
        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return self.country_name
        
class State(BaseModel):
    id = models.AutoField(primary_key=True)
    country_name = models.ForeignKey(Country,on_delete = models.CASCADE, related_name = 'country')
    state_name = models.CharField(max_length=30, unique = True)

    def save(self, *args, **kwargs):
        self.state_name = self.state_name.capitalize()
        super(State, self).save(*args, **kwargs)

    def __str__(self):
        return self.state_name
    
class City(BaseModel):
    id = models.AutoField(primary_key=True)
    state_name = models.ForeignKey(State, on_delete = models.CASCADE, related_name = 'state')
    city_name = models.CharField(max_length=30, unique = False)

    def clean(self):
        # Check if the state is with id=1 and city name is 'Hisar'
        if self.city_name and self.state_name:
            existing_cities =  City.objects.filter(city_name__iexact=self.city_name, state_name=self.state_name)
            if existing_cities.exists():
                raise ValidationError({'city_name':f'this city is already exist.'})
            
    def save(self, *args, **kwargs):
        self.full_clean()
        self.city_name = self.city_name.capitalize()
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.city_name

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=120)
    owner = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=10)
    telephone = models.CharField(max_length=10)
    mail_id = models.EmailField()

    # Address Details
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='client_country')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='client_states')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='client_city')
    district = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    pin_code = models.IntegerField()
    service_type= models.CharField(max_length=20)

    #Bank Details
    account_holder_name = models.CharField(max_length=50, verbose_name='A/C Holder Name')
    account_number = models.CharField(max_length=30)
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=11, verbose_name='IFSC Code')
    branch_name = models.CharField(max_length=50)
    pan_number = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=15, verbose_name='GSTIN Number')
    payment_terms= models.CharField(max_length=25)

    # Escalation Matrix

    # Contact Details
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    # documents
    address_proof = models.FileField(upload_to='documents/')
    company_proof = models.FileField(upload_to='documents/')
    cancelled_check = models.FileField(upload_to='documents/')
    gst_in = models.FileField(upload_to='documents/')
    pan_card = models.FileField(upload_to='documents/')
    attachment1 = models.FileField(upload_to='documents/')
    agreement = models.FileField(upload_to='documents/')
    tds_excemption_certificate = models.FileField(upload_to='documents/', verbose_name='TDS Excemption Certificate')

    
    

# Create your models here.


