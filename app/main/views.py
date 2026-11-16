from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login ,logout # Import as auth_login
from .forms import signInForm, signUpForm, addGoalForm, updateGoalForm, goalReflectionForm
from django.urls import reverse
from .models import Goals, Point, CompletedGoal
from django.contrib.auth.models import User

def Register(request):
    """
    Renders the signup page, displays the signup form,
    checks user credentials, and creates a new user.
    """

    if request.method == 'POST':
        signup_form = signUpForm(request.POST)

        if signup_form.is_valid():
            email = signup_form.cleaned_data["email"]
            password = signup_form.cleaned_data["password1"]
            confirm_password = signup_form.cleaned_data["password2"]

            if password == confirm_password:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already in use. Please log in.")
                else:
                    user = signup_form.save(commit=False)
                    user.set_password(password)  # Secure password
                    user.save()

                    Point.objects.create(user=user, my_point=0)  # Initialize user points

                    messages.success(request, "Signup successful! Please log in.")
                    return redirect('login')  # ✅ Redirect to login instead of 'home'
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "Invalid form submission. Please try again.")

    else:
        signup_form = signUpForm()

    return render(request, "main/signup.html", {'signup_form': signup_form})
# Citation for @login_required decorator:
# https://docs.djangoproject.com/en/5.1/topics/auth/default/#limiting-access-to-logged-in-users

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def logoutUserView(request):
    '''
    To logout the loggedin user from thier account
    when requested
    '''
    try:
        logout(request)
    except Exception as error:
        return HttpResponse(f"Error: {error}")
    # To redirect the user to signin page after logout
    return redirect('')


@login_required(login_url='login')
def homeView(request):
    '''
    To renders the goalsetting website home page
    '''
    try:
        # To query the users points
        my_points_instance = get_object_or_404(Point, user=request.user)
        # To get the users point for display
        my_point = my_points_instance.my_point
    except Exception as error:
        return HttpResponse(f"Error: {error}")
    return render(request, "main/home.html", {'my_point':my_point, 'user': request.user})


@login_required(login_url='login')
def addView(request):
    """
    Renders the 'Add Goal' page where users can add new goals.
    """
    try:
        if request.method == 'POST':
            add_goal_form = addGoalForm(request.POST)

            if add_goal_form.is_valid():
                add_goal = add_goal_form.save(commit=False)
                add_goal.user = request.user

                # Assign points based on goal importance
                importance_points = {
                    "High Importance": 40,
                    "Important": 25,
                    "Low Importance": 10
                }

                # Ensure goal importance is not empty
                goal_importance = add_goal.goal_importance
                if not goal_importance:
                    messages.error(request, "Goal importance cannot be blank.")
                    return render(request, "main/add.html", {'add_goal_form': add_goal_form})

                add_goal.goal_points = importance_points.get(goal_importance, 10)

                # Ensure goal category is not empty
                goal_category = add_goal.goal_category
                if not goal_category:
                    messages.error(request, "Goal category cannot be blank.")
                    return render(request, "main/add.html", {'add_goal_form': add_goal_form})

                # Assign goal category image
                goal_images = {
                    "Music": "main/images/music.jpeg",
                    "Sports": "main/images/sport.jpeg",
                    "Academics": "main/images/academic.jpeg",
                    "Money": "main/images/money.jpeg",
                    "Arts": "main/images/art.jpeg",
                    "Other": "main/images/other.jpeg",
                }
                add_goal.goal_category_image = goal_images.get(goal_category, "main/images/default.jpg")

                # Save the goal to the database
                add_goal.save()

                # Success message
                messages.success(request, "Goal added successfully!")
                return redirect("goals")  # Redirect to the goals page after success

            else:
                # If form is invalid, show error message
                messages.error(request, "There was an error with your submission. Please check your inputs.")

        else:
            add_goal_form = addGoalForm()  # GET request, show the empty form

        return render(request, "main/add.html", {'add_goal_form': add_goal_form})

    except Exception as error:
        # General exception error message
        messages.error(request, f"An error occurred: {error}")
        return render(request, "main/add.html", {'add_goal_form': addGoalForm()})



@login_required(login_url='login')
def goalView(request):
    """
    Renders the 'View Goals' page where users can see their goals.
    """
    try:
        # Retrieve user's goals from the database
        my_goals = Goals.objects.filter(user=request.user)
        goal_categories = ['Music','Sports','Academics','Money','Arts','Other']
        my_goals_categories = set()
        for goal in my_goals:
            my_goals_categories.add(goal.goal_category)
        missing_categories = set(goal_categories) - my_goals_categories

        if missing_categories:
            messages.warning(request, f"You haven't set goals for these categories: {', '.join(missing_categories)}")
        

        if not my_goals.exists():
            messages.warning(request, "You have no goals yet. Add a new goal to get started!")

    except NameError:
        messages.error(request, "Error: Incorrect Model Object name assigned.")
        return redirect("home")  # Redirect to home or another safe page

    except Exception as error:
        messages.error(request, f"An unexpected error occurred: {error}")
        return redirect("home")  

    return render(request, "main/goals.html", {"my_goals": my_goals})
    


@login_required(login_url='login')
def completeView(request):
    '''
    To renders the goalsetting website view 'Completed Goals'
    page through which users can mark thier goals as completed
    and add the proof of completion, upload files and write the
    goal/activity description and learning outcomes
    '''
    try:
        # to search and get the users goal object from the database
        my_goals = CompletedGoal.objects.filter(user=request.user)

    except Exception as error:
        return HttpResponse(f"Error: {error}")         

    return render(request, "main/completed.html", {"my_goals": my_goals})


@login_required(login_url='login')
def markCompletedView(request, goal_no):
    '''
    To render the mark complete (delete goal and add points)
    confirmation page.

    Parameters:
    1. goal_no: the assigned goal no in the database
    '''
    my_goals = Goals.objects.filter(user=request.user)
    my_goal_no = goal_no
    my_goal_instance = get_object_or_404(my_goals, pk=my_goal_no)

    try:
        
        # Get the user's points instance
        my_points_instance = get_object_or_404(Point, user=request.user)
        
        # Initialize the goal reflection form
        if request.method == "POST":
            goal_reflection_form = goalReflectionForm(request.POST)
            
            if goal_reflection_form.is_valid():
                # Update the user's points
                my_current_point = my_points_instance.my_point
                my_points_instance.my_point = my_current_point + my_goal_instance.goal_points
                my_points_instance.save()
                
                # Create and save the completed goal
                completed_goal = CompletedGoal(
                    user=request.user,
                    goal_name=my_goal_instance.goal_name,
                    add_date=my_goal_instance.add_date,
                    goal_description=my_goal_instance.goal_description,
                    goal_time=my_goal_instance.goal_time,
                    goal_requirements=my_goal_instance.goal_requirements,
                    goal_category=my_goal_instance.goal_category,
                    goal_category_image=my_goal_instance.goal_category_image,
                    goal_importance=my_goal_instance.goal_importance,
                    goal_points=my_goal_instance.goal_points,
                    goal_reflection=goal_reflection_form.cleaned_data['goal_reflection']
                )
                completed_goal.save()
                
                # Delete the goal since it's completed
                my_goal_instance.delete()
                
                return redirect('/completed')
        else:
            goal_reflection_form = goalReflectionForm()

                

        
    except Exception as error:
        return HttpResponse(f"Error: {error}")

    return render(request, "main/mark_completed.html", {'my_goals':my_goals,'my_goal_no':my_goal_no, 'my_goal_reflection_form': goal_reflection_form })



@login_required(login_url='login')
def UpdateGoalView(request, goal_no):
    """
    Allows users to update their goals without deleting them,
    ensuring points are not incremented on update.
    """
    try:
        # Fetch the goal instance for the current user
        my_goal_instance = get_object_or_404(Goals, pk=goal_no, user=request.user)
        my_goals = Goals.objects.filter(user=request.user)

        print(f"🎯 Goal {goal_no} found: {my_goal_instance.goal_name}")  # Debug

        if request.method == 'POST':
            update_goal_form = updateGoalForm(request.POST, instance=my_goal_instance)
            
            if update_goal_form.is_valid():
                update_goal = update_goal_form.save(commit=False)

                print(f"📝 Updating goal: {update_goal.goal_name}")  # Debug
                
                # Assign points based on goal importance
                importance_points = {
                    "High Importance": 40,
                    "Important": 25,
                    "Low Importance": 10
                }
                update_goal.goal_points = importance_points.get(update_goal.goal_importance, 10)

                print(f"🏆 Assigned points: {update_goal.goal_points}")  # Debug

                # Ensure goal category is not empty before processing
                if not update_goal.goal_category:
                    messages.error(request, "Goal category cannot be blank.")
                    return render(request, "main/update_goal.html", {
                        "my_goals": my_goals,
                        "my_goal_no": goal_no,
                        "update_goal_form": update_goal_form
                    })

                # Normalize goal category input
                goal_category = update_goal.goal_category.strip().title()
                print(f"📌 Goal Category before image assignment: {goal_category}")  

                # Assign category images only if it's empty (to prevent overwriting)
                goal_images = {
                    "Music": "main/images/music.jpeg",
                    "Sports": "main/images/sport.jpeg",
                    "Academics": "main/images/academic.jpeg",
                    "Money": "main/images/money.jpeg",
                    "Arts": "main/images/art.jpeg",
                    "Other": "main/images/other.jpeg",
                }

                # Ensure the path is correctly prefixed with `/static/`
                if not update_goal.goal_category_image:
                    update_goal.goal_category_image = f"/static/{goal_images.get(goal_category, 'main/images/default.jpg')}"

                print(f"🖼️ Assigned Image: {update_goal.goal_category_image}")  # Debug

                # Save updated goal
                update_goal.save()
                messages.success(request, "Goal updated successfully!")
                return redirect(reverse("goals"))  # Use Django's reverse() instead of hardcoded URL

            else:
                print(f"❌ Form errors: {update_goal_form.errors}")  # Debug
                messages.error(request, "Form submission failed. Please check the inputs.")

        else:
            update_goal_form = updateGoalForm(instance=my_goal_instance)
        
        return render(request, "main/update_goal.html", {
            "my_goals": my_goals,
            "my_goal_no": goal_no,
            "update_goal_form": update_goal_form
        })

    except (NameError, TypeError) as e:
        print(f"🚨 Variable or Type Error: {e}") 
        return HttpResponse(f"Error: {str(e)} - Check variable assignments and data types")

    except Exception as error:
        print(f"⚠️ Unexpected Error: {error}")
        messages.error(request, f"An unexpected error occurred: {error}")
        return render(request, "main/update_goal.html", {
            "my_goals": my_goals,
            "my_goal_no": goal_no,
            "update_goal_form": updateGoalForm(instance=my_goal_instance)
        })

