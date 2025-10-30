# Paste in: students/urls.py
# Adding new url for the feedback form

# students/urls.py
from django.urls import path
from . import views  # single import: use views.X everywhere

urlpatterns = [
    path("student/", views.StudentListView.as_view(), name="student-list-url"),
    path("section/", views.SectionListView.as_view(), name="section-list-url"),
    path("enrollment/", views.EnrollmentListView.as_view(), name="enrollment-list-url"),

    path("student/<int:primary_key>/", views.StudentDetail.as_view(),
         name="student-detail-url"),

    # Chart image endpoint
    path("charts/sections.png", views.section_counts_chart, name="chart-sections"),

    # New addition/change
    # Feedback form
    path("feedback/", views.feedback_view, name="feedback-url"),
]