from django.db.models import fields
from .models import Customer
from rest_framework import serializers

# Create your views here.


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
