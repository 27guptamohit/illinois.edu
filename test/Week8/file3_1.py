# Paste in: students/views.py
# New addition/changes: # New addition/changes: add_student()

from students.models import Student, Section, Enrollment
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from django.db.models import Count, Q

class StudentListView(ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "student_rows_for_looping"   # full list (handled automatically)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get("q")

        if q:
            search_qs = Student.objects.filter(first_name__icontains=q)
        else:
            search_qs = None
        ctx["q"] = q
        ctx["search_results"] = search_qs

        # =========================
        # MINI AGGREGATIONS (Also check the notes on the top for why we import Q.)
        # =========================
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
    template_name = "students/section_list.html"
    context_object_name = "section_rows_for_looping"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["students_per_section"] = (
            Section.objects
            .annotate(n_students=Count("section_related_name"))
            .values("code", "name", "n_students")
            .order_by("code")
        )
        ctx["students_per_term"] = (
            Section.objects
            .values("term")
            .annotate(n_students=Count("section_related_name"))
            .order_by("term")
        )
        # Example extra (if you want it later):
        ctx["enrollments_per_section"] = (
            Section.objects
            .annotate(
                n_enrolls=Count("enrollments_related_name"),
                n_active=Count("enrollments_related_name",
                               filter=Q(enrollments_related_name__is_active=True)),
            )
            .values("code", "n_enrolls", "n_active")
            .order_by("code")
        )
        return ctx

# New class
class EnrollmentListView(ListView):
    model = Enrollment
    context_object_name = "enrollment_rows_for_looping"

# views.py
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



#===============================================================================================
# Creating charts using matplotlib

from io import BytesIO
from django.http import HttpResponse

############ IMPORTANT
# Count is not one of our models.
# It’s a function (called an aggregate) that Django provides
# to perform SQL COUNT() operations inside queries.
from django.db.models import Count

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- CHART VIEW ----------
def section_counts_chart(request):
    # Count how many students belong to each section
    # (Student.section has related_name='section_related_name')
    data = (
        Section.objects
        .annotate(student_count=Count("section_related_name"))
        .order_by("code")
    )

    labels = [sec.code for sec in data]
    counts = [sec.student_count for sec in data]

    # fig: the whiteboard, and
    # ax:  the rectangle you actually draw on.
    fig, ax = plt.subplots(figsize=(6, 3), dpi=150)

    # .bar:
    #   •	This is Matplotlib’s method for creating a bar chart.
    # 	•	It draws rectangular bars based on x values (labels) and heights (counts).
    ax.bar(labels, counts, color="#13294B")  # Illinois Blue

    ax.set_title("Students per Section", fontsize=10, color="#13294B")

    ax.set_xlabel("Section", fontsize=8)
    ax.set_ylabel("Students", fontsize=8)

    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)

    # tight_layout() automatically adjusts the spacing between chart elements like:
    # 	•	the axes labels (x/y),
    # 	•	the title,
    # 	•	and the plot area (bars, ticks, etc.)
    # so that nothing gets cut off when you save or display the figure.

    # Without tight_layout(), Matplotlib often leaves awkward margins
    # or chops text off the edges when saving to an image file.
    fig.tight_layout()

    # BytesIO()
    # 	•	It lets you create a temporary file-like object, but stored in memory, not on disk.
    # 	•	Think of it as a fake file drawer that lives in RAM.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    plt.close(fig)
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type="image/png")

#=======================================================
from .forms import FeedbackForm


# Define a view function that handles both GET (show form)
# and POST (process submission) requests
def feedback_view(request):

    # Check the HTTP method.
    # If the user clicked the Submit button, the browser sends a POST request.
    if request.method == "POST":

        # Create a FeedbackForm object and "bind" it to the submitted data.
        # request.POST is a dictionary of the form’s input names and values.
        form = FeedbackForm(request.POST)

        # Validate the form (runs Django’s built-in + custom field checks).
        if form.is_valid():

            # If valid, get the cleaned (validated and converted) data.
            # cleaned_data is a dictionary with safe, normalized values.
            data = form.cleaned_data

            # For demo purposes: printing the feedback to the console.
            # In a real project, you might save it, email it, or redirect.
            print("Name:", data["name"], "Feedback:", data["feedback"])

    # If the request is NOT POST (first visit or refresh), use a blank form.
    else:
        form = FeedbackForm()

    # Render the template with a context dictionary containing the form.
    # Django will send this HTML back to the user’s browser.
    # - On GET: shows an empty form.
    # - On POST (invalid): shows the form again with error messages.
    # - On POST (valid): here, still re-renders (you could redirect instead).
    return render(request, "students/feedback.html", {"form": form})



#===================================================================================================
# Import the StudentForm class that we defined in forms.py
from django.shortcuts import redirect
from .forms import StudentForm

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()               # ← automatic DB save
            return redirect("student-list-url")
    else:
        form = StudentForm()
    return render(request, "students/add_student.html", {"form": form})

#===================================================================================================
# New addition/changes: new import + Generic Class based views
from django.views.generic import CreateView
# reverse_lazy is a lazy version of reverse() — it delays URL resolution until it’s actually needed.
# reverse_lazy() defers evaluation until it’s actually needed (i.e., when the view runs).
# Use reverse_lazy() inside class-based views (CBVs).
# Use reverse() inside functions (FBVs).
from django.urls import reverse_lazy


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm        # or: fields = ["first_name", ...]
    template_name = "students/add_student.html"
    success_url = reverse_lazy("student-list-url")  # go back to list after save
