from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class AbsGoal(models.Model):
    '''
    Abstract Base class for goals tables
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    goal_name = models.CharField(max_length=200)
    add_date = models.DateTimeField(default=timezone.now)
    goal_description = models.CharField(max_length=1500)
    goal_time = models.CharField(max_length=30)
    goal_requirements = models.CharField(max_length=250)
    
    class GoalCategory(models.TextChoices):
        MUSIC = 'Music', _('Music')
        SPORTS = 'Sports', _('Sports')
        ACADEMICS = 'Academics', _('Academics')
        MONEY = 'Money', _('Money')
        ARTS = 'Arts', _('Arts')
        OTHER = 'Other', _('Other')

    goal_category = models.CharField(max_length=50, choices=GoalCategory.choices)
    #Citation: https://docs.djangoproject.com/en/5.1/ref/models/fields/#enumeration-types

    goal_category_image = models.CharField(max_length=150, default="main/images/image-default")
    
    class GoalImportance(models.TextChoices):
        LOW = 'Low Importance', _('Low Importance')
        MEDIUM = 'Important', _('Important')
        HIGH = 'High Importance', _('High Importance')

    goal_importance = models.CharField(max_length=50, choices=GoalImportance.choices)
    goal_points = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Goals(AbsGoal):
    '''
    To create a table for storing goals
    '''
    def __str__(self):
        return self.goal_name

    
class Point(models.Model):
    '''
    Creates a table for storing points.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    my_point = models.IntegerField(default=0)

    def __str__(self):
        return str(self.my_point)
    
class CompletedGoal(AbsGoal):
    '''
    Creates a table to store completed goals.
    '''
    goal_reflection = models.CharField(max_length=2500, null=True)


    def __str__(self):
        return self.goal_name
