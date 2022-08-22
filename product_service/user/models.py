from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=False)
    gender = models.CharField(
        max_length=140,
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
    )
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=254)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} - {self.first_name}"

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}".strip()
        return f"{self.first_name} {self.last_name}".strip()
