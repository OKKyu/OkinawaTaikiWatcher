from django.contrib import admin

# Register your models here.
from .models import Criterias, Settings, Kyokus

admin.site.register(Criterias)
admin.site.register(Settings)
admin.site.register(Kyokus)
