# Create new file in the master settings directory: illinois/views.py


# Step 1: Create the root view.
from django.shortcuts import redirect

def redirect_root_view(request):

    # If you go to css/urls.py, we entered name='student-list-url' for the url 'student/'
    # Here, instead of writing the 'student/', we are referencing its 'reference name'.
    # These reference names are like nicknames or petnames (analogically).
    # The name of the person may change, but they may continue to be called by the same nickname by friends and family.

    # You can also write: return redirect('student/')
    # But in case, if you change to new url 'student/' to 'students_new/'
    # and if you forget to change its reference here, then the website will not redirect the user to the intended pattern.

    return redirect('student-list-url')

# Step 2:
# Go to illinois/urls.py or file1_2.py
# Import this view there.