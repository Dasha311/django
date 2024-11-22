from django.contrib import admin
from . import models


admin.site.register(models.Dish)
admin.site.register(models.Restaurant)
admin.site.register(models.Menu)
admin.site.register(models.Courier)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Customer)
admin.site.register(models.Payment)
admin.site.register(models.WorkingHours)
admin.site.register(models.SpecialHours)