# Paste in: students/urls.py
# New addition/changes: # New addition/changes: api_students(); api_ping()

from django.urls import path
from . import views  # single import: use views.X everywhere
from .views import StudentCreateView

urlpatterns = [
    path("student/", views.StudentListView.as_view(), name="student-list-url"),
    path("section/", views.SectionListView.as_view(), name="section-list-url"),
    path("enrollment/", views.EnrollmentListView.as_view(), name="enrollment-list-url"),

    path("student/<int:primary_key>/", views.StudentDetail.as_view(),
         name="student-detail-url"),

    # Chart image endpoint
    path("charts/sections.png", views.section_counts_chart, name="chart-sections"),

    path("feedback/", views.feedback_view, name="feedback-url"),
    # New addition/change
    # Feedback form Student model
    path("function-add-student/", views.add_student, name="function-add-student-url"),

    path("class-add-student/", StudentCreateView.as_view(), name="class-add-student-url"),

    # New addition/changes
# JSON endpoints (Week 9)
    path("api/ping-httpresponse/", views.api_ping_httpresponse, name="api-ping-httpresponse"),
    path("api/ping-json/", views.api_ping_jsonresponse, name="api-ping-json"),
    path("api/function-students/", views.api_students, name="api-students"),

]