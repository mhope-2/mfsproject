from django.db import models

class Quotations(models.Model):
    quotation_no = models.CharField(max_length=255)
    user_id = models.PositiveBigIntegerField()
    customer_id = models.PositiveBigIntegerField()
    customer_first_name = models.CharField(max_length=255)
    customer_middle_name = models.CharField(max_length=255, blank=True, null=True)
    customer_last_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    issued_by = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "{}".format(self.quotation_no)


class QuotationItems(models.Model):
    quotation_no = models.CharField(max_length=255) 
    product_id = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "{}".format(self.quotation_no)

