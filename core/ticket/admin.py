from django.contrib import admin
from .models import Ticket, Purchase, Review, Favorite

admin.site.register(Ticket)
admin.site.register(Purchase)
admin.site.register(Review)
admin.site.register(Favorite)
