# Paste in: css/views.py
# We are now creating new List views for Section and Enrollment

from students.models import Student, Section, Enrollment
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView


class StudentListView(ListView):
    model = Student
    context_object_name = "student_rows_for_looping"

# New class
class SectionListView(ListView):
    model = Section
    context_object_name = "section_rows_for_looping"

# New class
class EnrollmentListView(ListView):
    model = Enrollment
    context_object_name = "enrollment_rows_for_looping"


class StudentDetail(View):

    def get(self, request, primary_key):
        student = get_object_or_404(Student, pk=primary_key)
        enrollments = student.enrollments_related_name.all()

        return render(
            request,
            'students/student_detail.html',
            {
                'single_student_var_for_looping': student,
                'enrollments_var_for_looping': enrollments,
            },
        )

