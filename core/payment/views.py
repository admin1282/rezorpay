from rest_framework import mixins, generics
from .models import Payment
from .serializers import PaymentSerializer, PaymentHistorySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Create your views here.
class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]


class PaymentHistoryListAPIView(generics.ListAPIView):
    serializer_class = PaymentHistorySerializer
    queryset = Payment.objects.all().order_by('-id')
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
    # pagination_class = StandardResultSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset


class PaymentHistoryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentHistorySerializer
    queryset = Payment.objects.all()
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]