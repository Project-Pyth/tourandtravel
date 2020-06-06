from django.contrib import admin
from myapp3.models import packages_tour
admin.site.register(packages_tour)
# Register your models here.
from myapp3.models import userprofile, contact, booking_detail
admin.site.register(userprofile)
admin.site.register(contact)
admin.site.register(booking_detail)
