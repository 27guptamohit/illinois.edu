# Paste in: css/views.py
# First import the two new libraries Count

from students.models import Student, Section, Enrollment
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

# New import

# Q is a helper class in Django’s ORM that lets you build more complex query filters.
# Normally, you write queries like:

### Student.objects.filter(first_name__icontains="Alice", last_name__icontains="Smith")

# That always combines with AND.
# But what if you want OR, or conditional logic? That’s where Q comes in.

# Example usage of Q:
###### Find css whose first name contains Alice OR whose nickname contains Alice
###### Student.objects.filter(
######                         Q(first_name__icontains="Alice") | Q(nickname__icontains="Alice")
######                        )

# Without Q, Django only allows AND joins. With Q, you can use:
# 	•	| for OR
# 	•	& for AND (explicit)
# 	•	~ for NOT

from django.db.models import Count, Q


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

            ## why use the double underscores after a field name or related name of a field?
            ## This is called Django’s double-underscore (ORM lookup) syntax.
            search_qs = Student.objects.filter(first_name__icontains=q)
        else:
            search_qs = None

        # 4. Add our own variables to the context / get_context_data
        ctx["q"] = q
        ctx["search_results"] = search_qs

        # =========================
        # MINI AGGREGATIONS (Also check the notes on the top for why we import Q.)
        # =========================
        # Goal: show tiny summaries that are easy to explain to undergrads.

        # A) Overall totals
        #    - Count of all css
        #    - Count of all enrollments
        ctx["total_students"] = Student.objects.count()
        ctx["total_enrollments"] = Enrollment.objects.count()

        # B) Students per Section
        #    Section <--(reverse to Student via related_name='section_related_name')
        #    We get: code, name, and how many css are linked to that section.
        ctx["students_per_section"] = (
            Section.objects
            .values("code", "name")
            .annotate(n_students=Count("section_related_name"))
            .order_by("code")
        )

        # C) Enrollments per Section (plus "active" enrollments)
        #    Section <--(reverse to Enrollment via related_name='enrollments_related_name')
        #    We count all enrollments, and also only the ones where is_active=True.
        ctx["enrollments_per_section"] = (
            Section.objects
            .values("code")
            .annotate(
                n_enrolls=Count("enrollments_related_name"),
                n_active=Count("enrollments_related_name",

                               # Here:
                               # 	•	Q(enrollments_related_name__is_active=True) means “only count enrollments where is_active is true.”
                               # 	•	Without Q, you’d count all enrollments, not just the active ones.
                               filter=Q(enrollments_related_name__is_active=True)),
            )
            .order_by("code")
        )

        # D) Students per Term
        #    'term' lives on Section; each Student belongs to a Section.
        #    Count how many css are in sections for each term.
        ctx["students_per_term"] = (
            Section.objects
            .values("term")
            .annotate(n_students=Count("section_related_name"))
            .order_by("term")
        )

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

