# Changes in: illinois/urls.py
"""
Here, I feel to make the url structure more organized.
By that I mean, keep only the top level urls which are common to master settings
and to the entire website here.
Rest all the urls go to their respective applications/features.

Instructions:
1. Delete all the application/feature related urls from here.
2. Only keep all the admin related urls here.
3. This page will only have master level urls and not app specific ones.
4. Using the include(css.urls), create a shortcut/reference to urls of the features.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
]
