from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(List)
admin.site.register(Task)
admin.site.register(Dependancy)
