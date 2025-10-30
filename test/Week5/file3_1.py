# paste this in css/views.py

""""
A. Function Based View (Covered in Week 4):

A.1. Using HttpResponse() method:

def student_list_view(request):
    student_list_query = Student.objects.all()
    context = {'student_list_html': student_list_query}
    template = loader.get_template('css/student_list.html')
    output = template.render(context)
    return HttpResponse(output)


--------------------------
A.2. Using render(method):

def student_list_view(request):

    student_list_query = Student.objects.all()
    context = {'student_list_html': student_list_query}
    return render(request, 'css/student_list.html', context)

====================
B. Class Based View (using the render method):

We will implement the same render method that we covered in A.2.
"""
from django.shortcuts import render

from students.models import Student

# create a new import for: django.views import View
from django.views import View

# Method 1: View
# Observe that here we are importing View and not ListView
class StudentListView(View):

    # get is the method that will handle the incoming Http requests
    # bonus: what is the difference between method vs functions?
    # If a function is within a class, it is called a method.
    def get(self, request):
        return render(
            request,                                                       # Listing the request received
            'students/student_list.html',                    # Providing the name of html where to send this data
            context={'student_list_html': Student.objects.all()}           # Importing the rows of the table
        )

