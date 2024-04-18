from django.db import models
from django.contrib.auth.models import User
from app.models import Tikit
# Create your models here.



class PaymentMethod(models.IntegerChoices):
    card = 1, 'card'
    upi = 2, 'upi'
    netbanking = 3, 'netbanking'
    wallet = 4, 'wallet',
    cardless_emi = 5, 'cardless_emi'


class PaymentStatus(models.IntegerChoices):
    pending = 1, 'Pending'
    cancelled = 2, 'Cancelled'
    partially_paid = 3, 'Partially Paid'
    paid = 4, 'Paid'
    failed = 5, 'Failed'
    refund = 6, 'Refund'


class Order(models.Model):
    order_id = models.CharField(max_length=250, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True) # first time instance created time create ans does not update ones create
    modified = models.DateTimeField(auto_now=True) # it track last modified object and save
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order_id}'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tikits = models.ForeignKey(Tikit, on_delete=models.CASCADE,null=True,default=None)
    payment_method = models.PositiveSmallIntegerField(choices=PaymentMethod.choices, null=True,default=None)
    payment_status = models.PositiveSmallIntegerField(choices=PaymentStatus.choices, default=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, default=None)
    transaction_id = models.CharField(max_length=250, null=True, blank=True,default=None)
    amount = models.FloatField()
    vpa = models.CharField(max_length=250, null=True, blank=True,default=None)
    bank = models.CharField(max_length=250, null=True, blank=True,default=None)
    wallet = models.CharField(max_length=250, null=True, blank=True,default=None)
    card_id = models.CharField(max_length=250, null=True, blank=True,default=None)
    refund_id = models.CharField(max_length=250, null=True, blank=True,default=None)
    created = models.DateTimeField(auto_now_add=True) # first time instance created time create ans does not update ones create
    modified = models.DateTimeField(auto_now=True) # it track last modified object and save
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.amount} | {self.transaction_id}'

    def set_order(self, order):
        self.order = order
        self.save()


class CardInformation(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT)
    name = models.CharField(max_length=250)
    last4 = models.CharField(max_length=4)
    network = models.CharField(max_length=25)
    type = models.CharField(max_length=10)
    issuer = models.CharField(max_length=10)
    international = models.BooleanField()
    emi = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True) # first time instance created time create ans does not update ones create
    modified = models.DateTimeField(auto_now=True) # it track last modified object and save
    deleted = models.BooleanField(default=False)