# To be pasted in: css/views.py
# I'm now building on top of file5_1_optional.py


# Step 1: Import the View
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from students.models import Student


class StudentListView(ListView):
    model = Student
    context_object_name = "student_rows_for_looping"

# define a new view class for showing one student
class StudentDetail(View):


    def get(self, request, primary_key):

        # First, get the Student table from the models.py
        # then get the id of the student from the url entered by the user: website.com/student/<pk>
        student = get_object_or_404(Student, pk=primary_key)

        # Now, check models.py and in it check the Enrollment class.
        # Over there, I defined the related_name as 'enrollments_related_name'
        # this helped us to tell Django to get all the data from Enrollments table just for this student.
        enrollments = student.enrollments_related_name.all()

        # Return an HTTP response by rendering the HTML template.
        # We pass a dictionary (context) so the template can access student and enrollments data.
        return render(
            request,                                             # the original HTTP request
            'students/student_detail.html',         # path to the template
            {
                'single_student_var_for_looping': student,              # single student object
                'enrollments_var_for_looping': enrollments,      # list of all enrollment records for this student
            },
        )




