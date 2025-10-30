# Paste in illinois/urls.py (master settings)

from django.contrib import admin
from django.urls import path, include

# ---------- Step 1: Import your view function ----------
# Here we import the student_list_view function
# from the css/views.py file so we can connect it to a URL.
from students.views import student_list_view


# ---------- Step 2: Define the URL patterns ----------
# urlpatterns is a list that tells Django:
#   • which URL to listen for
#   • and which view function to call when that URL is visited
urlpatterns = [
    # URL pattern 1 → Admin site
    # Visiting http://127.0.0.1:8000/admin/ opens the built-in Django admin
    path('admin/', admin.site.urls),

    # URL pattern 2 → Students list
    # Visiting http://127.0.0.1:8000/students/ will call the student_list_view function
    # which queries the database, loads the template, and returns the response
    path('css/', student_list_view),
]