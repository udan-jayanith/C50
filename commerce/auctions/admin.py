from django.contrib import admin
from auctions.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comments)
admin.site.register(Bid)

