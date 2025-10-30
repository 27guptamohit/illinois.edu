# Paste in: css/views.py
# We are now expanding StudentListView to get the search query and return the search results.

from students.models import Student, Section, Enrollment
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView


class StudentListView(ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "student_rows_for_looping"   # full list (handled automatically)


    # **kwargs means “any extra keyword arguments.”
    # Example analogy:
    # 	•	Sometimes you bring home only bread.
    # 	•	Sometimes bread + milk + apples.
    # 	•	Instead of writing a function that only accepts “bread,” you say “I’ll accept whatever groceries you bring me.”
    def get_context_data(self, **kwargs):

        # 1. Get the default context (already includes all css)
        # Django by default has get_context_data() function. It contains all the data from the current class.
        # The data like model, template_name, context_object_name
        # But by creating a new function on the top [def get_context_data(self, **kwargs)], we are overriding the default function and creating our own data on top of already existing data.

        # super():
        # super() lets you call the parent class’s method inside your child class.
        # 	•	StudentListView inherits from ListView.
        # 	•	ListView already has its own get_context_data() that prepares the student list.
        # 	•	We override get_context_data(), but we don’t want to throw away the default behavior.
        # Analogically it says: please also run the parent’s version of get_context_data() and give me its result, so I can add more stuff.

        # Another example analogy:
        # Imagine your mom packs your school bag with notebooks and pencils. You want to add a snack.
        # 	•	If you don’t call super(), you start with an empty bag → only snack.
        #	•	If you call super(), you get her bag (with notebooks and pencils), then add your snack.
        ctx = super().get_context_data(**kwargs)

        # 2. Grab the search term from the request
        # In the html, the data would have been collected in:
        # <input type="search"
        #        name="q"
        #        value="{{ q }}"
        #        class="form-control"
        #        placeholder="Search by first name">
        # This input tag lives inside the <form> tag in html.
        #
        q = self.request.GET.get("q")

        # 3. If there is a search term, filter css by first name
        if q:
            search_qs = Student.objects.filter(first_name__icontains=q)
        else:
            search_qs = None

        # 4. Add our own variables to the context / get_context_data
        ctx["q"] = q
        ctx["search_results"] = search_qs

        return ctx

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

