# paste this in css/views.py

from django.shortcuts import render
from .models import Student

def student_list_view(request):
    """
    A function-based view that:
    1. Queries all Student rows from the database.
    2. Passes them into a context dictionary.
    3. Uses Django's render() shortcut to:
       - load the 'css/student_list.html' template
       - fill it with the context data
       - and return the rendered HTML inside an HttpResponse.
    """

    # ---------- Step 1: Query all Student rows ----------
    student_list_query = Student.objects.all()

    # ---------- Step 2: Store results in a context dictionary ----------
    context = {'student_list_html': student_list_query}

    # ---------- Step 3: Use render() shortcut ----------
    return render(request, 'students/student_list.html', context)