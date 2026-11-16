from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.login_view, name="login"),  # Login page
    path("register/", views.Register, name="register"),  # Signup page
    path("home/", views.homeView, name="home"),  # Home page
    path("logout/", views.logout_view, name="logout"),  # Logout
    path("add/", views.addView, name="add"),  # Add new goal
    path("goals/", views.goalView, name="goals"),  # View goals
    path("completed/", views.completeView, name="completed"),  # Completed goals
    path("markcompleted/<int:goal_no>/", views.markCompletedView, name="markcompleted"),  # Mark goal as completed
    path("update/<int:goal_no>/", views.UpdateGoalView, name="update"),  # Update goal
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)