# Create new file in the master settings directory: illinois/views.py


# Step 1: Create the root view.
from django.shortcuts import redirect

def redirect_root_view(request):
    return redirect('student-list-url')

# Step 2:
# Go to illinois/urls.py or file1_2.py
# Import this view there.