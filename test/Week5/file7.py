# Paste in: css/urls.py

from django.urls import path, include

# Step 1: Import the StudentList & StudentDetail class
from students.views import (StudentListView,
                            StudentDetail)

# Step 2: define the url
# Check slides of week 5 to see the purpose of 'name'.
urlpatterns = [
    path('student/',
         StudentListView.as_view(),
         name='student-list-url'),


    path('student/<int:primary_key>/',
         StudentDetail.as_view(),
         name='student-detail-url'),

]
