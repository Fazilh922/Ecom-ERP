from django.db import models
from paymentapp.models import Transaction

class OrderTracking(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])
    updated_at = models.DateTimeField(auto_now=True)
