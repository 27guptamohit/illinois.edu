# Run with:
# python manage.py shell < test/Week11/file1_1_dummy_data/fill_dummy.py

from students.models import Section, Student, Enrollment

# ---- Section (safe to re-run) ----
sec1, _ = Section.objects.get_or_create(
    code="INFO-590-MG",
    defaults={"name": "Web App Dev III", "term": "Fall 2026"},
)

# ---- Choose EXACTLY 24 students ----
# Remove TWO of the last four to keep 24 total (I marked DROP options).
students_data = [
    ("David", "Kim", "", "david.kim@example.com", sec1),
    ("Eve", "Patel", "Evie", "eve.patel@example.com", sec1),
    ("Frank", "Garcia", "", "frank.garcia@example.com", sec1),
    ("Grace", "Hernandez", "Gracie", "grace.hernandez@example.com", sec1),
    ("Hank", "Nguyen", "", "hank.nguyen@example.com", sec1),
    ("Ivy", "Wong", "", "ivy.wong@example.com", sec1),
    ("Jack", "Brown", "", "jack.brown@example.com", sec1),
    ("Kara", "Wilson", "", "kara.wilson@example.com", sec1),
    ("Leo", "Martinez", "", "leo.martinez@example.com", sec1),
    ("Maya", "Adams", "", "maya.adams@example.com", sec1),
    ("Noah", "Clark", "", "noah.clark@example.com", sec1),
    ("Olivia", "Davis", "Liv", "olivia.davis@example.com", sec1),
    ("Paul", "Rodriguez", "", "paul.rodriguez@example.com", sec1),
    ("Quinn", "Lopez", "", "quinn.lopez@example.com", sec1),
    ("Rita", "Gonzalez", "", "rita.gonzalez@example.com", sec1),
    ("Sam", "Perez", "", "sam.perez@example.com", sec1),
    ("Tina", "Hughes", "", "tina.hughes@example.com", sec1),
    ("Uma", "Sanders", "", "uma.sanders@example.com", sec1),
    ("Victor", "Murphy", "", "victor.murphy@example.com", sec1),
    ("Wendy", "Foster", "", "wendy.foster@example.com", sec1),
    ("Xavier", "Bennett", "", "xavier.bennett@example.com", sec1),
    ("Yara", "Cruz", "", "yara.cruz@example.com", sec1),
    ("Zane", "Mitchell", "", "zane.mitchell@example.com", sec1),
    ("Ava", "Reed", "", "ava.reed@example.com", sec1),
    # ("Ben", "Carter", "", "ben.carter@example.com", sec1),   # DROP to keep 24
    # ("Chloe", "Long", "", "chloe.long@example.com", sec1),   # DROP to keep 24
]

created_students = 0
for first, last, nick, email, sec in students_data:
    stu, made = Student.objects.get_or_create(
        email=email,  # unique natural key
        defaults={
            "first_name": first,
            "last_name": last,
            "nickname": nick,
            "section": sec,
        },
    )
    created_students += int(made)
    # ensure enrollment exists (unique per (student, section))
    Enrollment.objects.get_or_create(student=stu, section=sec)

print(f"Students created this run: {created_students}")
print("Sections:", Section.objects.count())
print("Students:", Student.objects.count())
print("Enrollments:", Enrollment.objects.count())