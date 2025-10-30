# paste this in css/views.py

from django.http import HttpResponse
from django.template import loader

# ---------- Step 1: Import the Student table ----------
# To read from the Student table, we need to import it here.
# Since models.py is in the same folder, we use '.' before 'models'.
# This tells Python to look for the file in the same directory.
from .models import Student


# This function runs whenever the website receives a request
# related to the Student table. It will process the code inside.

def student_list_view(request):
    """
    A function-based view that:
    1. Queries all Student rows from the database.
    2. Passes them into a context dictionary.
    3. Loads the 'css/student_list.html' template.
    4. Renders the template with the context.
    5. Returns the rendered HTML inside an HttpResponse.
    """

    # ---------- Step 2: Fetch all the rows from the Student table ----------
    # Query all Student objects from the database
    student_list_query = Student.objects.all()

    # ---------- Step 3: Save all the data into a context dictionary ----------
    # Pass the student_list into the template context
    context = {'student_list_html': student_list_query}

    # OPTIONAL:
    # If you uncomment the line below, no rows will be imported.
    # On the HTML page, it will show "no css".
    # Try commenting out the 'student_list_query' above and using this instead.
    # student_list_query = Student.objects.none()

    # ---------- Step 4: Load the HTML template ----------
    #  • Load the HTML template file
    #  • Fill it with your context variables (student_list_html)
    #  • Get back a string of HTML (output)
    #  • Finally, wrap it in an HttpResponse to send to the browser
    template = loader.get_template('students/student_list.html')

    # ---------- Step 5: Render the template with the context ----------
    output = template.render(context)

    # ---------- Step 6: Return the final HttpResponse ----------
    return HttpResponse(output)