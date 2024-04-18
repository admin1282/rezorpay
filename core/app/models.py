from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class PurchaseStatus(models.IntegerChoices):
    Pending = 1, 'Pending'
    Confirmed = 2, 'Confirmed'
    OnHold = 3, 'On Hold'
    Cancelled = 4, 'Cancelled'

class PaymentStatus(models.IntegerChoices):
    Pending = 1, 'Pending'
    PartiallyPaid = 2, 'Partially Paid'
    Paid = 3, 'Paid'
    Failed = 4, 'Failed'

class Tikit(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.PositiveSmallIntegerField(choices=PaymentStatus.choices, default=1)
    purchase_status = models.PositiveSmallIntegerField(choices=PurchaseStatus.choices, null=True,default=None)
    created = models.DateTimeField(auto_now_add=True) # first time instance created time create ans does not update ones create
    modified = models.DateTimeField(auto_now=True) # it track last modified object and save
    deleted = models.BooleanField(default=False)
