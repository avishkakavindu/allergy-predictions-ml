from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    """ Hold patient details """

    FEMALE = NO = 0
    MALE = YES = 1
    NOT_AWARE = 2

    GENDER = [
        (FEMALE, 'Female'),
        (MALE, 'Male')
    ]

    HAVE_ALLERGIES = [
        (NO, 'No'),
        (YES, 'Yes'),
        (NOT_AWARE, 'Not Aware')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=1, null=True, blank=True)
    sex = models.PositiveSmallIntegerField(choices=GENDER, default=MALE)
    allergies = models.PositiveIntegerField(choices=HAVE_ALLERGIES, default=NO)
    family_history = models.BooleanField(default=False)
    drug_allergies = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class FoodType(models.Model):
    """ HOld food type details """

    food_type = models.CharField(max_length=255)

    def __str__(self):
        return self.food_type


class Food(models.Model):
    """ Hold food details """

    food = models.CharField(max_length=255, null=False, blank=False)
    food_type = models.ForeignKey(FoodType, on_delete=models.CASCADE)

    def __str__(self):
        return self.food


class Reference(models.Model):
    """ Food references(allergy related) """

    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.food.food
