# Run this script with:

# Just in case the uploaded db.sqlite3 is not having any of the dummy data (I doubt that will be the case),
# run the below line to fill in the dummy data.
# This code will auto-populate the dummy data into the db.sqlite3.

### Run this line in terminal:
# python manage.py shell < test/Week4/file1_1_dummy_data/fill_dummy.py

from students.models import Section, Student, Enrollment

# Clear existing data (optional, for clean runs)
Section.objects.all().delete()
Student.objects.all().delete()
Enrollment.objects.all().delete()

# ---------- Step 1: Create Sections ----------
sec1 = Section.objects.create(code="INFO-390-MG", name="Web App Dev I", term="Fall 2025")
sec2 = Section.objects.create(code="INFO-490-MG", name="Web App Dev II", term="Spring 2026")

print("Sections created:", Section.objects.all())

# ---------- Step 2: Create Students ----------
alice = Student.objects.create(
    first_name="Alice",
    last_name="Johnson",
    nickname="AJ",
    email="alice@example.com",
    section=sec1
)

bob = Student.objects.create(
    first_name="Bob",
    last_name="Smith",
    email="bob@example.com",
    section=sec1
)

carol = Student.objects.create(
    first_name="Carol",
    last_name="Lee",
    email="carol@example.com",
    section=sec2
)

print("Students created:", Student.objects.all())

# ---------- Step 3: Create Enrollments ----------
Enrollment.objects.create(student=alice, section=sec1)
Enrollment.objects.create(student=bob, section=sec1)
Enrollment.objects.create(student=carol, section=sec2)

print("# # # # # # \nDummy data inserted successfully!")
print("Sections:", Section.objects.count())
print("Students:", Student.objects.count())
print("Enrollments:", Enrollment.objects.count())