from django.contrib import admin
from . import models


admin.site.register(models.Client)
admin.site.register(models.Company)
admin.site.register(models.Agent)
admin.site.register(models.User)