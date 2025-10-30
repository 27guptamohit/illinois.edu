# Changes in: illinois/urls.py
# We are now adding a link for the home page.

from django.contrib import admin
from django.urls import path, include
from illinois.views import redirect_root_view


urlpatterns = [

    # Here, we are trying to create a view that will be our home page.
    # That is why we are not pointing it any 'app_name/urls.py', but towards our own view.
    path('', redirect_root_view),

    path('admin/', admin.site.urls),
    path('', include('students.urls')),     # css/urls.py
]
