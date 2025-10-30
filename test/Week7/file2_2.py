# Paste in: students/urls.py
# Let's add url for charts

from django.urls import path, include

# Step 1: Import chart view
from .views import section_counts_chart



from students.views import (StudentListView, SectionListView, EnrollmentListView,
                            StudentDetail)

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

# Paste in: css/urls.py
    path('student/<int:primary_key>/',
         StudentDetail.as_view(),
         name='student-detail-url'),

# Step 2: define the url
# New addition/change: url for charts
    path("charts/sections.png",
         section_counts_chart,                     # FUNCTION VIEW
         name="chart-sections"),


]
