from django.contrib import admin
from .models import Goals, Point, CompletedGoal

# To display the goals in admin pannel
admin.site.register(Goals)
# To display the points in admin pannel
admin.site.register(Point)
# To display the points in admin pannel
admin.site.register(CompletedGoal)
