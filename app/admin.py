from django.contrib import admin

from .models import Category,Sub_Category,Brand,Product,Contact_us,Order
# Register your models here.

admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Contact_us)
admin.site.register(Order)
