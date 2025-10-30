# Here, you'll see this printed in terminal:
# '9 objects imported automatically (use -v 2 for details).'

# 	This is because Django’s shell pre-imports some utilities so you don’t have to type them manually each time.

##### What are those 9 objects?
# They are shortcuts Django gives you (from django.db.models and related). For example:
# 	•	Q (for complex queries)
# 	•	F (for field references)
# 	•	Count, Sum, Avg, Max, Min (aggregation functions)
# 	•	maybe datetime helpers, depending on version

# In plain language, Django is saying:
# 'I preloaded 9 handy objects for you. Run with -v 2 if you want to see the exact list.'

######## Imp: If you want to see what are these handy objects, run this:
# python manage.py shell -v 2 < test/Week4/file1_1_dummy_data/test_file.py

# '-v 2' stands for '-verbosity {level}' and tells Django: 'Be more verbose - show me details about what you’re importing.'

# Django can print different amounts of detail depending on the verbosity level you set:
# 	•	-v 0 → silent mode (only critical errors)
# 	•	-v 1 → default (normal output, minimal info)
# 	•	-v 2 → more detailed output (extra info, lists things Django is doing for you)
# 	•	-v 3 → debug-level verbosity (most detailed, internal SQL queries, etc.)

a = 1+1
print(a)