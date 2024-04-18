import random

import razorpay
from django.db import transaction
from razorpay import Client
from rest_framework import serializers

from django.conf import settings
from .models import Payment, Order, CardInformation
from .razorpay import FetchRazorPayByOrder
from rest_framework.exceptions import ValidationError
from app.serializers import TikitSerializer
from app.models import Tikit
client: Client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def random_number():
    return str(random.randint(0, 9999))


class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(write_only=True)

    class Meta:
        model = Order
        exclude = ['created', 'modified', 'deleted']

    def create(self, validated_data: dict):
        validated_data['amount'] = int(validated_data['amount']) * 100
        data = {'amount': str(validated_data['amount']), 'currency': "INR"}

        # update order_id
        validated_data.update(self.create_order(data))
        return super().create(validated_data)

    @staticmethod
    def create_order(data):
        order = client.order.create(data, )
        return {"order_id": order.get("id")}


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardInformation
        exclude = ['created', 'modified', 'deleted']


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(required=False, write_only=True)
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    tikit_id = serializers.PrimaryKeyRelatedField(queryset=Tikit.objects.all(), write_only=True, source="tikits")
    amount = serializers.FloatField(required=True)
    card = CardSerializer(source='cardinformation', read_only=True)
    transaction_id = serializers.CharField(trim_whitespace=True, required=False)
    payment_status_str = serializers.CharField(source='get_payment_status_display', read_only=True)
    payment_method_str = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Payment
        exclude = ['created', 'modified', 'deleted']

    def validate(self, attrs):
        user = self.context.get('request').user
        from django.contrib.auth.models import AnonymousUser
        if isinstance(user, AnonymousUser):
            raise ValidationError("User not authenticated or authorized.")
        attrs['user'] = user
        return attrs

    def create(self, validated_data: dict):
        mobile = None
        amount = {'amount': validated_data.pop('amount')}
        create_order = OrderSerializer(data=amount)
        if create_order.is_valid(raise_exception=True):
            create_order.save()

        # load razorpay data from API
        razor_pay_by_order = FetchRazorPayByOrder(client=client, order=create_order.data['order_id'],
                                                  purchase_model=self.Meta.model)
        # set payment status
        validated_data['payment_status'] = razor_pay_by_order.get_payment_status_by_order()

        '''
        create payment in db and set it here to attach it to purchase model
        Razorpay sends amount 500.00 as 50000, so divided by 100 in order to get the correct amount.
        '''
        validated_data['amount'] = (razor_pay_by_order.response_data_by_order['amount'] / 100)

        instance = super().create(validated_data)
        instance.save()


        # set order on payment
        v = Order.objects.filter(id=create_order.data['id']).last()
        instance.set_order(v)
        return instance


    @transaction.atomic()
    def update(self, instance, validated_data: dict):
        transaction_id = instance.order.order_id
        razor_pay = FetchRazorPayByOrder(client=client, order=transaction_id,
                                         purchase_model=self.Meta.model)

        if razor_pay.response_data_by_payment:
            instance.amount = razor_pay.response_data_by_payment['amount'] / 100
            instance.transaction_id = razor_pay.response_data_by_payment['id']
            instance.payment_status = razor_pay.get_payment_status_by_payment()
            instance.payment_method = razor_pay.get_payment_method()
            instance.save()

            tikits_instance = instance.tikits
            if tikits_instance:
                if instance.payment_status == 1:
                    tikits_instance.payment_status = 1
                    tikits_instance.purchase_status = 1

                elif instance.payment_status == 3:
                    tikits_instance.payment_status = 2
                    tikits_instance.purchase_status = 3

                elif instance.payment_status == 4:
                    tikits_instance.payment_status = 3
                    tikits_instance.purchase_status = 2

                elif instance.payment_status == 5:
                    tikits_instance.payment_status = 4

                else:
                    pass

                tikits_instance.save()
        else:
            instance.amount = 0
            instance.transaction_id = ''
            instance.payment_status = 5
            instance.save()
        return instance


class CardInformationSerializer(serializers.ModelSerializer):
    payment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CardInformation
        exclude = ['created', 'modified', 'deleted']


class BaseOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['created', 'modified', 'deleted']


class PaymentHistorySerializer(serializers.ModelSerializer):
    tikits = TikitSerializer(read_only=True)
    order = BaseOrderSerializers(read_only=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", source='created', read_only=True, required=False)
    date_created = serializers.SerializerMethodField()
    time_created = serializers.SerializerMethodField()
    class Meta:
        model = Payment
        fields = ['id', 'payment_method', 'transaction_id', 'tikits', 'order', 'created_at', 'date_created', 'time_created']


    def get_date_created(self, obj):
        return obj.created.date()

    def get_time_created(self, obj):
        return obj.created.time()