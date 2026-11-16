from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Goals, CompletedGoal

class signInForm(forms.Form):
    '''
    For taking user(registerd) credentials at "main/signin.html"
    '''
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={'class':'Login-form-input', 'placeholder':'Enter your username'}))
    password = forms.CharField(max_length=1000,label="Password",widget=forms.PasswordInput(attrs={'class':'Login-form-input', 'placeholder':'Enter you password'}))

class signUpForm(UserCreationForm):
    '''
    For taking new user credentials at "main/signup.html"
    '''
    username = forms.CharField(max_length=150, label="", widget=forms.TextInput(attrs={'class':'Login-form-input', 'placeholder':'Username'}))
    email = forms.EmailField(max_length=150, label="", widget=forms.TextInput(attrs={'class':'Login-form-input', 'placeholder':'Email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(signUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = 'Username:'
        self.fields['username'].help_text = ''

        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = 'Email:'
        self.fields['email'].help_text = ''

        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['class'] = "Login-form-input"
        self.fields['password1'].label = 'Password:'
        self.fields['password1'].help_text = ''

                
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['class'] = 'Login-form-input'
        self.fields['password2'].label = 'Confirm Password:'
        self.fields['password2'].help_text = ''


class addGoalForm(forms.ModelForm):
    '''
    To add take and add new goal that is to be added to the database. 
    '''
    goal_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': "add-goal-form-input"}))
    goal_description = forms.CharField(max_length=1500, widget=forms.TextInput(attrs={'class': "add-goal-form-input"}))
    goal_requirements = forms.CharField(max_length=1500, widget=forms.TextInput(attrs={'class': "add-goal-form-input"}))
    goal_category = forms.ChoiceField(choices=Goals.GoalCategory.choices)
    goal_importance = forms.ChoiceField(choices=Goals.GoalImportance.choices)
    goal_time = forms.CharField(widget=forms.TextInput(attrs={'id':'goal_deadline', 'class': "add-goal-form-input"}))

    class Meta:
        model = Goals
        fields = ['goal_name', 'goal_description', 'goal_requirements', 'goal_category', 'goal_importance', 'goal_time',]
        # to exclude these in the form
        exclude = ("user","goal_points", "goal_category_image")

        def __init__(self, *args, **kwargs):
            super(signUpForm, self).__init__(*args, **kwargs)

            self.fields['goal_time'].widget.attrs['placeholder'] = 'Don not enter anything click on selection month'
            self.fields['goal_time'].label = 'Goal Deadline:'
            self.fields['goal_time'].help_text = ''

class updateGoalForm(forms.ModelForm):
    '''
    To update goals in case the user want to make changes to the goals after creating them!
    '''
    goal_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': "add-goal-form-input"}))
    goal_description = forms.CharField(max_length=1500, widget=forms.TextInput(attrs={'class': "add-goal-form-input"}))
    goal_time = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'id':'goal_deadline','class': "add-goal-form-input"}))
    goal_requirements = forms.CharField(max_length=1500, widget=forms.TextInput(attrs={'class': "add-goal-form-input"}))
    goal_category = forms.ChoiceField(choices=Goals.GoalCategory.choices)
    goal_importance = forms.ChoiceField(choices=Goals.GoalImportance.choices)

    class Meta:
        model = Goals
        fields = ['goal_name', 'goal_description', 'goal_requirements', 'goal_category', 'goal_importance', 'goal_time',]
        # to exclude these in the form
        exclude = ("user","goal_points", "goal_category_image")

        def __init__(self, *args, **kwargs):
            super(signUpForm, self).__init__(*args, **kwargs)

            self.fields['goal_time'].widget.attrs['placeholder'] = 'Don not enter anything click on selection month'
            self.fields['goal_time'].label = 'Goal Deadline:'
            self.fields['goal_time'].help_text = ''



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class goalReflectionForm(forms.ModelForm):
    '''
    To add reflection and learning outcomes from a goal.
    '''
    goal_reflection = forms.CharField(max_length=2500,  widget=forms.Textarea(attrs={'class': "goal_reflection_textarea"}))


    class Meta:
        model = CompletedGoal
        fields = ['goal_reflection']
        # to exclude these in the form
        exclude = ("user","goal_name","goal_description", "goal_points", "add_date", "goal_requirements","goal_category","goal_importance", "goal_time","goal_category_image",)

        def __init__(self, *args, **kwargs):
            super(signUpForm, self).__init__(*args, **kwargs)
            
            self.fields['goal_reflection'].widget.attrs['placeholder'] = 'Enter your learning outcomes'
            self.fields['goal_reflection'].label = 'Learning Outcomes:'
            self.fields['goal_reflection'].help_text = ''