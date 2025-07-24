from django.contrib import admin
from accounts.models import *

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(UserAddress)
