from django.contrib import admin
from .models import *


admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(HealthProblem)
admin.site.register(Answer)
admin.site.register(Comment)
