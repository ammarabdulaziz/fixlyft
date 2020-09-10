from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.urls import reverse
from fixlyft_project.utils import unique_slug_generator
from django.db.models.signals import pre_save
#from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from fixlyft_project.utils import IntegerRangeField
# Create your models here.
phone_regex = RegexValidator(regex = r'^[7-9][0-9]{9}$')

SERVICES_CHOICES = (
    ('0', 'SELECT_SERVICES'),
    ('Smartphone / Tablet', 'Smartphone / Tablet'),
    ('Laptop / Pc', 'Laptop / Pc'),
    ('Gaming Consoles', 'Gaming Consoles'),
)

class MobileShop(models.Model):
    shop_name = models.CharField(max_length=50)
    shop_img = models.ImageField(default='default.png', upload_to='shop_images', help_text="Please Upload Image in 90x90 pixels size only for better view")
    slug = models.SlugField(max_length=200, null=True, blank=True)
    rating = IntegerRangeField(min_value=1, max_value=5, default=1)
    city_name = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=15)
    phone = models.CharField(validators = [phone_regex], max_length=12)
    date_added = models.DateTimeField(default=timezone.now)
    services = models.CharField(choices=SERVICES_CHOICES, max_length=30, default=None)
    premium = models.BooleanField(default=False)

    class Meta:
        ordering = ['-premium', '-rating']


    def __str__(self):
        return self.shop_name

    
    def get_absolute_url(self):
        return reverse('schedule', kwargs={'pk': self.pk})

#    def save(self, *args, **kwargs):
#        super().save(*args, **kwargs)
 #       img = Image.open(self.shop_img.path)
 #       if img.height > 90 or img.width > 90:
  #          output_size = (90, 90)
  #          img.thumbnail = (output_size)
  #          img.save(self.shop_img.path)

    @property
    def ImageUrl(self):
        try:
            url = self.shop_img.url
        except:
            url = ''
        return url


class PickUP(models.Model):
    customer_name = models.CharField(max_length=30)
    mobileshop = models.ForeignKey(MobileShop, on_delete=models.CASCADE, null=True)
    mobile_number = models.CharField(validators = [phone_regex], max_length=12)
    device_name = models.CharField(max_length=50)
    complaint = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now) 

    class Meta:
        ordering = ['-timestamp',] 


    def __str__(self):
        return self.customer_name

    def get_absolute_url(self):
        return reverse('schedule')

class SmsOTP(models.Model):
    phone = models.CharField(validators = [phone_regex], max_length = 15, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    validated = models.BooleanField(default=False, help_text='True if OTP is verified')
    otp_session_id = models.CharField(max_length=120, null=True, default="")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)

class OfferImages(models.Model):
    link = models.URLField(max_length=999)
    offer_img = models.ImageField(default='c.png', upload_to='offer_images', help_text="Please upload images in 660x300 pixels only for better view")
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_added']

    
#    def save(self, *args, **kwargs):
 #       super().save(*args, **kwargs)
#        img = Image.open(self.offer_img.path)
#        if img.height > 660 or img.width > 300:
#            output_size = (660, 300)
#            img.thumbnail = (output_size)
  #          img.save(self.offer_img.path)

    @property
    def ImageUrl(self):
        try:
            url = self.offer_img.url
        except:
            url = ''
        return url


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=MobileShop)
