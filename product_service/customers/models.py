from django.db import models


# create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=191)
    middle_name = models.CharField(max_length=191, blank=True, null=True)
    last_name = models.CharField(max_length=191)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=191)
    address = models.CharField(max_length=191, blank=True, null=True)
    customer_code = models.CharField(max_length=10, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_code}"

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}".strip()
        return f"{self.first_name} {self.last_name}".strip()
