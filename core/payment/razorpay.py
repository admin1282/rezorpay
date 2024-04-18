from payment.models import Order


def get_payment_status_id(data):
    if data['status'] == 'captured':
        return 4

    elif data['status'] == 'authorized':
        return 1

    elif data['status'] == 'failed':
        return 5

    elif data['status'] == 'refunded':
        return 6

    elif data['status'] == 'created':
        return 1


def get_payment_method_id(data):
    if data['method'] == 'card':
        return 1

    elif data['method'] == 'upi':
        return 2

    elif data['method'] == 'netbanking':
        return 3

    elif data['method'] == 'wallet':
        return 4

    elif data['method'] == 'cardless_emi':
        return 5


class FetchRazorPayByOrder:
    def __init__(self, purchase_model, client, order):
        self.client = client
        self.purchase_model = purchase_model
        self.order: Order = order
        self.response_data_by_payment = self.get_razorpay_payment_response(order)
        self.response_data_by_order = self.get_razorpay_order_response(order)

    def get_razorpay_payment_response(self, order):
        data = self.client.order.payments(order)
        if data['items']:
            data = data['items'][0]
            return data
        return []

    def get_razorpay_order_response(self, order):
        return self.client.order.fetch(order)

    def get_payment_status_by_payment(self):
        return get_payment_status_id(self.response_data_by_payment)

    def get_payment_status_by_order(self):
        return get_payment_status_id(self.response_data_by_order)

    def get_payment_method(self):
        return get_payment_method_id(self.response_data_by_payment)