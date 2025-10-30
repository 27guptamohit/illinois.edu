# Changes in: illinois/urls.py
# # new addition/changes: LoginView

from django.contrib import admin

# new addition/changes: New import
from django.contrib.auth.views import LoginView

from django.urls import path, include
from illinois.views import redirect_root_view


urlpatterns = [

    # Here, we are trying to create a view that will be our home page.
    # That is why we are not pointing it any 'app_name/urls.py', but towards our own view.
    path('', redirect_root_view),

    path('admin/', admin.site.urls),

    path('', include('students.urls')),     # css/urls.py

    # new addition/changes: LoginView
    path('login/',
         LoginView.as_view(template_name='students/login.html'),
         name='login_urlpattern'),

]
