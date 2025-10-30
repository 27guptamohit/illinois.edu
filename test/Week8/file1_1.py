# Paste in: students/forms.py
# New File

from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=50, label="Your Name")
    email = forms.EmailField(label="Email Address")
    feedback = forms.CharField(widget=forms.Textarea, label="Comments")