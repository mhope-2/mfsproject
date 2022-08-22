from django.db import models
# from product_service.customers.models import Customer
# from product_service.user.models import User

# # Create your models here.
class Invoices(models.Model):
    invoice_no = models.CharField(max_length=255, unique=True)
    quotation_no = models.CharField(max_length=255) 
    user_id = models.PositiveBigIntegerField()
    customer_id = models.PositiveBigIntegerField()
    customer_first_name = models.CharField(max_length=255)
    customer_middle_name = models.CharField(max_length=255, blank=True, null=True)
    customer_last_name = models.CharField(max_length=255, blank=True, null=True)
    net_total = models.DecimalField(decimal_places=2, max_digits=10)
    customer_phone = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)

    amount_received = models.DecimalField(decimal_places=2, max_digits=10)
    cash = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    bank_transfer = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    mobile_money = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    
    issued_by = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "{}".format(self.invoice_no)


class InvoiceItems(models.Model):
    invoice_id = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField() 
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10,decimal_places=2)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    date_refunded = models.DateTimeField(blank=True, null=True)


    class Meta:
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return "{}".format(self.invoice_no)
