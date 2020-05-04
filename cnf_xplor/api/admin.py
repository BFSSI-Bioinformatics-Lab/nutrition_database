from django.contrib import admin

# Register your models here.
from django.contrib import admin
from cnf_xplor.api import models
# Register your models here.
admin.site.register(models.Food)
admin.site.register(models.Nutrient)
admin.site.register(models.ConversionFactor)
