from rest_framework import serializers
from .models import Invoices, InvoiceItems

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoices
        # fields = '__all__'
        exclude = ['quotation_no']

class InvoiceItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItems
        fields = '__all__'
