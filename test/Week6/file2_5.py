# Paste in: css/urls.py
# Let's add the new urls for section and the enrollment

from django.urls import path, include

# Step 1: Import the StudentList & StudentDetail class
from students.views import (StudentListView, SectionListView, EnrollmentListView,
                            StudentDetail)

# Step 2: define the url
# Check slides of week 5 to see the purpose of 'name'.
urlpatterns = [
    path('student/',
         StudentListView.as_view(),
         name='student-list-url'),

    path('section/',
         SectionListView.as_view(),
         name='section-list-url'),

    path('enrollment/',
         EnrollmentListView.as_view(),
         name='enrollment-list-url'),


    path('student/<int:primary_key>/',
         StudentDetail.as_view(),
         name='student-detail-url'),

]
