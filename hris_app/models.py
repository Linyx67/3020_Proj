from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Overriding the Default Django User To add a 'user_type' field


# This code defines a custom user model called `CustomUser` that inherits from the built-in
# `AbstractUser` model provided by Django.
class CustomUser (AbstractUser):

    # Constants representing the different user types
    ADMINISTRATOR = '1'
    STAFF = '2'

    # A dictionary to map email addresses to user types
    EMAIL_TO_USER_TYPE_MAP = {
        'administrator': ADMINISTRATOR,
        'staff': STAFF
    }

    # A tuple containing the available user types and their display names
    user_type_data = ((ADMINISTRATOR, "Administrator"), (STAFF, "Staff"))

    # A field to store the user's type, with a default value of '1' (ADMINISTRATOR)
    user_type = models.CharField(
        default=1,
        choices=user_type_data,
        max_length=20
    )

# models for the User Login information


class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StaffUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will
# automatically insert data in Admin or Staff
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:

        # Check the user_type and insert the data in respective tables
        if instance.user_type == '1':
            AdminUser.objects.create(admin=instance)
        if instance.user_type == '2':
            StaffUser.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == '1':
        instance.adminuser.save()
    if instance.user_type == '2':
        instance.staffuser.save()
