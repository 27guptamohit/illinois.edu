# Step 1: css/models.py

from django.db import models

# ---------- Parent table ----------
class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    code       = models.CharField(max_length=10, unique=True)
    name       = models.CharField(max_length=60)
    term       = models.CharField(max_length=16, blank=True)


# ---------- Child table ----------
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name  = models.CharField(max_length=45)
    nickname   = models.CharField(max_length=45, blank=True, default="")
    email      = models.EmailField(unique=True)
    section    = models.ForeignKey(Section, on_delete=models.PROTECT, related_name="learners")

# ---------- Association table (join table) ----------
class Enrollment(models.Model):
    enroll_id   = models.AutoField(primary_key=True)
    student     = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    section     = models.ForeignKey(Section, on_delete=models.PROTECT, related_name="enrollments")
    enrolled_on = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)


