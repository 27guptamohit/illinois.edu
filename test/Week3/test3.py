# Step 3: css/models.py
# Now run makemigrations and migrate commands separately

from django.db import models


# ---------- Parent table ----------
class Section(models.Model):
    section_id    = models.AutoField(primary_key=True)

    code  = models.CharField(max_length=10, unique=True)   # e.g. "CS101-A"
    name  = models.CharField(max_length=60)                # e.g. "Intro to CS - A"
    term  = models.CharField(max_length=16, blank=True)    # e.g. "Fall 2025"

    class Meta:
        # Ordering type: ascending
        # Order by single column
        # or: ["code", "name"]
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} ({self.term or '—'})"


# ---------- Child table ----------
class Student(models.Model):
    student_id         = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=45)
    last_name  = models.CharField(max_length=45)

    # If you remove blank=True, a value is required in forms.
    # default="" inserts an empty string if no input is given.
    nickname   = models.CharField(max_length=45, blank=True, default="")

    # unique: Even though email is not the primary key, it must be unique globally.
    email      = models.EmailField(unique=True)

    #================================================
    # IMPORTANT: ONE-TO-MANY RELATIONSHIP
    # Many css belong to one section.
    #
    # on_delete options:
    # - models.PROTECT → prevents deleting a Section if css still belong to it.
    # - models.CASCADE → deleting a Section will also delete all related css.
    #
    # Section: This is the model's name to which the current model class is referencing.
    #
    # related_name: It’s the name Django will use for the reverse relation
    # (i.e., how the parent model can access its children).
    # Without related_name: Django uses the default <modelname>_set.

    # Very Important
    #     Example: s = Section.objects.get(code="CS101-A")          # Select all the rows where the 'code' column has value = "CS101-A"
    #              s.student_set.all()                              # reverse lookup (default name); here, Student class = student_set

    # With related_name: You define your own name instead of student_set.
    #     Example: s.learners.all()                                 # give me all the css registered in 'CS101-A'
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,   # start safe; try changing this to CASCADE after class
        related_name="learners",
    )

    class Meta:
        # Ordering shown automatically in admin & querysets
        ordering = ["last_name", "first_name"]

        # implies restrictions on what kind of data can be entered.
        # here, no data can be entered with existing first_name + last_name + section.
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name", "section"],

                # The name="uniq_student_name_in_section" is simply a label for the uniqueness rule at the database level.
                # It doesn’t affect how you query in Django, but it makes database errors, schema, and migrations human-readable.
                name="uniq_student_name_in_section",
            )
        ]

    def __str__(self):
        base = f"{self.last_name}, {self.first_name}"
        return f"{base} ({self.nickname})" if self.nickname else base


# ---------- Association table (join table) ----------
class Enrollment(models.Model):
    enroll_id       = models.AutoField(primary_key=True)

    # FK → Student (child side of Student; Enrollment belongs to a Student)
    student  = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,   # if a student is removed, remove their enrollments
        related_name="enrollments"
    )

    # FK → Section (child side of Section; Enrollment belongs to a Section)
    section  = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,   # protects Sections with enrollments; demo flip to CASCADE to compare
        related_name="enrollments"
    )

    # Additional attributes often seen on an enrollment record
    enrolled_on = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        # Ordering: newest first, then by student name for stable presentation
        # Adding a - sign in front of '-enroll_id' flips the order to descending order.
        ordering = ["-enroll_id", "student__last_name", "student__first_name"]

        # Prevent duplicate enrollments for the same student+section pair
        constraints = [
            models.UniqueConstraint(
                fields=["student", "section"],
                name="uniq_enrollment_per_student_per_section",
            )
        ]

    def __str__(self):
        return f"Enrollment(student={self.student_id}, section={self.section_id})"
