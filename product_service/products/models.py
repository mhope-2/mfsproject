from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    unit = models.CharField(
        max_length=140,
        choices=(("PCS", "PCS"), ("PCK", "PCK")),
        default="PCS",
    )

    quantity = models.PositiveIntegerField()
    barcode = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "{}".format(self.name)
