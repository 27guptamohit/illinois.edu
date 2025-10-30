# Paste in: students/views.py
# addition/changes: Cleaned and organized version of views.py

# =======================================================================================
# IMPORTS
# =======================================================================================

# --- Week 4 / 5: Core Django + Models / Querysets / Aggregations ---
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse, reverse_lazy
from datetime import datetime
import csv
import json
import urllib.request

# --- Week 6 / 7: Visualization and external data (matplotlib, requests) ---
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import requests

# --- Week 11: Export / Download, API-style JSON endpoints ---
# (already covered above: JsonResponse, csv, datetime, json)

# --- Week 12: Authentication / LoginRequired / Signup flow ---
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms_auth import StudentSignUpForm

# --- Forms (Week 10 form handling) ---
from .forms import FeedbackForm, StudentForm

# --- Our models (Week 3 data modeling and after) ---
from students.models import Student, Section, Enrollment


# =======================================================================================
# WEEK 12: AUTHENTICATED LIST / DETAIL PAGES (LoginRequiredMixin on CBVs)
# - StudentListView
# - SectionListView
# - EnrollmentListView
# - StudentDetail
# =======================================================================================

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "student_rows_for_looping"
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get("q")

        if q:
            search_qs = Student.objects.filter(first_name__icontains=q)
        else:
            search_qs = None

        ctx["q"] = q
        ctx["search_results"] = search_qs
        ctx["total_students"] = Student.objects.count()
        ctx["total_enrollments"] = Enrollment.objects.count()

        ctx["students_per_section"] = (
            Section.objects
            .values("code", "name")
            .annotate(n_students=Count("section_related_name"))
            .order_by("code")
        )

        ctx["enrollments_per_section"] = (
            Section.objects
            .values("code")
            .annotate(
                n_enrolls=Count("enrollments_related_name"),
                n_active=Count(
                    "enrollments_related_name",
                    filter=Q(enrollments_related_name__is_active=True)
                ),
            )
            .order_by("code")
        )

        ctx["students_per_term"] = (
            Section.objects
            .values("term")
            .annotate(n_students=Count("section_related_name"))
            .order_by("term")
        )

        return ctx


class SectionListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = "students/section_list.html"
    context_object_name = "section_rows_for_looping"
    redirect_field_name = 'next'

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

        ctx["enrollments_per_section"] = (
            Section.objects
            .annotate(
                n_enrolls=Count("enrollments_related_name"),
                n_active=Count(
                    "enrollments_related_name",
                    filter=Q(enrollments_related_name__is_active=True)
                ),
            )
            .values("code", "n_enrolls", "n_active")
            .order_by("code")
        )

        return ctx


class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    context_object_name = "enrollment_rows_for_looping"
    redirect_field_name = 'next'


class StudentDetail(LoginRequiredMixin, View):
    redirect_field_name = 'next'

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


# =======================================================================================
# WEEK 10: FORMS (Feedback form + Add student form + CreateView)
# - feedback_view()
# - add_student()
# - StudentCreateView
# =======================================================================================

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print("Name:", data["name"], "Feedback:", data["feedback"])
    else:
        form = FeedbackForm()

    return render(request, "students/feedback.html", {"form": form})


@login_required(login_url='login_urlpattern')
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student-list-url")
    else:
        form = StudentForm()
    return render(request, "students/add_student.html", {"form": form})


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/add_student.html"
    success_url = reverse_lazy("student-list-url")
    redirect_field_name = 'next'


# =======================================================================================
# WEEK 11: JSON API ENDPOINTS + DATA EXPORT (CSV / JSON downloads)
# - api_students(), api_students_per_section(), api_enrollments_per_section()
# - api_ping_jsonresponse(), api_ping_httpresponse(), StudentsAPI
# - export_students_csv(), export_students_json()
# =======================================================================================

def api_students(request):
    q = (request.GET.get("q") or "").strip()
    qs = Student.objects.all().values(
        "student_id", "first_name", "last_name",
        "nickname", "email", "section__code"
    )

    if q:
        qs = Student.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(nickname__icontains=q)
        ).values(
            "student_id", "first_name", "last_name",
            "nickname", "email", "section__code"
        )

    data = list(qs.order_by("last_name", "first_name"))
    return JsonResponse({"count": len(data), "results": data})


def api_students_per_section(request):
    rows = (
        Section.objects
        .annotate(n_students=Count("section_related_name"))
        .values("code", "n_students")
        .order_by("code")
    )

    labels = [r["code"] for r in rows]
    counts = [r["n_students"] for r in rows]
    return JsonResponse({"labels": labels, "counts": counts})


def api_enrollments_per_section(request):
    rows = (
        Section.objects
        .annotate(
            n_all=Count("enrollments_related_name"),
            n_active=Count(
                "enrollments_related_name",
                filter=Q(enrollments_related_name__is_active=True)
            ),
        )
        .values("code", "n_all", "n_active")
        .order_by("code")
    )
    return JsonResponse({"results": list(rows)})


def api_ping_jsonresponse(request):
    return JsonResponse({"ok": True})


def api_ping_httpresponse(request):
    payload = json.dumps({"ok": True})
    payload2 = json.loads(payload)
    return HttpResponse(payload2, content_type="application/json")


class StudentsAPI(LoginRequiredMixin, View):
    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        qs = Student.objects.all()
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(nickname__icontains=q)
            )
        data = list(
            qs.values(
                "student_id", "first_name", "last_name",
                "nickname", "email", "section__code"
            ).order_by("last_name", "first_name")
        )
        return JsonResponse({"count": len(data), "results": data})


@login_required(login_url='login_urlpattern')
def export_students_csv(request):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"students_{timestamp}.csv"

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["student_id", "first_name", "last_name", "email", "section_code"])

    rows = (
        Student.objects
        .select_related("section")
        .values_list("student_id", "first_name", "last_name", "email", "section__code")
        .order_by("last_name", "first_name")
    )

    for row in rows:
        writer.writerow(row)

    return response


@login_required(login_url='login_urlpattern')
def export_students_json(request):
    data = list(
        Student.objects
        .select_related("section")
        .values(
            "student_id",
            "first_name",
            "last_name",
            "email",
            "section__code"
        )
        .order_by("last_name", "first_name")
    )

    json_content = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "record_count": len(data),
        "students": data,
    }

    response = JsonResponse(json_content, json_dumps_params={"indent": 2})

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"students_{timestamp}.json"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    return response


# =======================================================================================
# WEEK 9: REPORTING PAGES (HTML summary dashboards)
# - ReportsView
# =======================================================================================

class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "students/reports.html"
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["students_per_section"] = (
            Section.objects
            .values("code", "name")
            .annotate(n_students=Count("section_related_name"))
            .order_by("code")
        )
        ctx["enrolls_per_section"] = (
            Section.objects
            .annotate(
                n_all=Count("enrollments_related_name"),
                n_active=Count(
                    "enrollments_related_name",
                    filter=Q(enrollments_related_name__is_active=True)
                ),
            )
            .values("code", "n_all", "n_active")
            .order_by("code")
        )
        return ctx


# =======================================================================================
# WEEK 8: MATPLOTLIB CHART VIEWS (server-generated PNGs)
# - section_counts_chart()
# - EnrollmentsChartPage
# - enrollments_chart_png()
# =======================================================================================

@login_required(login_url='login_urlpattern')
def section_counts_chart(request):
    data = (
        Section.objects
        .annotate(student_count=Count("section_related_name"))
        .order_by("code")
    )

    labels = [sec.code for sec in data]
    counts = [sec.student_count for sec in data]

    fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
    ax.bar(labels, counts, color="#13294B")
    ax.set_title("Students per Section", fontsize=10, color="#13294B")
    ax.set_xlabel("Section", fontsize=8)
    ax.set_ylabel("Students", fontsize=8)
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type="image/png")


class EnrollmentsChartPage(LoginRequiredMixin, TemplateView):
    template_name = "students/enrollments_chart.html"


@login_required(login_url='login_urlpattern')
def enrollments_chart_png(request):
    api_url = request.build_absolute_uri(reverse("api-enrollments-per-section"))

    with urllib.request.urlopen(api_url) as resp:
        payload = json.load(resp)

    rows = payload.get("results", [])

    labels        = [r["code"] for r in rows]
    all_counts    = [r["n_all"] for r in rows]
    active_counts = [r["n_active"] for r in rows]

    x = range(len(labels))
    width = 0.4

    fig, ax = plt.subplots(figsize=(6.5, 3.2), dpi=150)
    ax.bar([i - width/2 for i in x], all_counts,   width=width, label="All",    color="#13294B")
    ax.bar([i + width/2 for i in x], active_counts, width=width, label="Active", color="#E84A27")

    ax.set_title("Enrollments per Section")
    ax.set_ylabel("Enrollments")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type="image/png")


# =======================================================================================
# WEEK 8.5: EXTERNAL API CALL (requests to Open-Meteo)
# - WeatherNow
# =======================================================================================

class WeatherNow(LoginRequiredMixin, View):
    redirect_field_name = 'next'

    def get(self, request):
        params = {
            "latitude": 40.1164,
            "longitude": -88.2434,
            "current_weather": True,
        }

        try:
            output_raw_all = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params=params,
                timeout=5
            )

            output_raw_all.raise_for_status()
            output_polished_all = output_raw_all.json()
            output_polished_cw_only = output_polished_all.get("current_weather", {})

            return JsonResponse({"ok": True, "weather": output_polished_cw_only})

        except requests.exceptions.RequestException as e:
            return JsonResponse({"ok": False, "error": str(e)}, status=502)


# =======================================================================================
# WEEK 12 (Part 2): PUBLIC SIGNUP FLOW
# - signup_view()
#   (create account, auto-login, redirect)
# =======================================================================================

def signup_view(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("student-list-url")
    else:
        form = StudentSignUpForm()

    return render(request, "students/signup.html", {"form": form})