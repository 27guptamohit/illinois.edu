# New file: css/urls.py
""""
Instructions:
1. Copy the illinois/urls.py.
2. Paste it in css. The file should now exist as css/urls.py
3. In it, keep all the urls specific to this current application/feature.
4. Delete all the admin related urls from here.
"""

from django.urls import path, include
from students.views import student_list_view

urlpatterns = [
    path('css/', student_list_view),
]
