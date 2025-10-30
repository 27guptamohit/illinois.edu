# Important: Use this only if you want to change the variable name for data sent to HTML.
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
from django.views.generic import ListView

from students.models import Student

# create a new import for: django.views import View
from django.views import View

# Method 2: ListView
# Observe that here we are importing ListView and not View
# Important: This will only work if the template is named correctly:
############ <model_name>list.html

# If the name of the template is different, then use this:
# template_name = "<template directory>/new_name.html"

# Eg:
# template_name = "css/your_custom_name.html"

# If you want to give custom name to your 'objects/rows of tables', then you can use this:
# context_object_name = "student_rows_for_looping"   # custom name
# context_object_name = "student_rows_for_looping"

# If you don't use context_object_name, then the default import name would be:
#### 'object_list' for looping purpose in the html


class StudentListView(ListView):
    model = Student
    context_object_name = "student_rows_for_looping"

    # template_name = "css/your_custom_name.html"         # optional: if you've different html file name


