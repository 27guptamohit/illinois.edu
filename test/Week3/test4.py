# Step 5: Register the models in css/admin.py
# Now do runserver.

from django.contrib import admin
from .models import Section, Student, Enrollment

admin.site.register(Section)
admin.site.register(Student)
admin.site.register(Enrollment)