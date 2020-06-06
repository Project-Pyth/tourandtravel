from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now



class Profilee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profilee.objects.create(user=instance)
        instance.profilee.save()

class packages_tour(models.Model):
    package_id = models.AutoField
    place_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default ="")
    cost = models.IntegerField()
    desc = models.CharField(max_length=2000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='packages_pics')

    def __str__(self):
        return self.place_name

class userprofile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,primary_key = True)
    contact = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    image = models.ImageField(upload_to = 'packages_pics',null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userprofile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


#class book(models.Model):
    #name = models.CharField(max_length=50)
    #contact = models.CharField(max_length=50,default ="")
    #address = models.CharField(max_length=200)
    #email = models.CharField(max_length=200)
    #city = models.CharField(max_length=200)
    #state = models.CharField(max_length=200)
    #from_date = models.DateField(default=now)
    #to_date = models.DateField(null=True, blank=True)


class contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default ="")
    phone = models.CharField(max_length=50, default ="")
    desc = models.CharField(max_length=500, default="")

class booking_detail(models.Model):
    b_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50,default ="")
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    from_date = models.DateField(default=now)
    to_date = models.DateField(null=True, blank=True)

