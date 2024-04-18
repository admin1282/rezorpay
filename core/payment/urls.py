from django.urls import path
from . import views


urlpatterns = [
    path('payment/history', views.PaymentHistoryListAPIView.as_view()),
    path('payment/history/<int:pk>/', views.PaymentHistoryRetrieveAPIView.as_view()),
    path('payment/pay/', views.PaymentCreateAPIView.as_view()),
    path('payment/pay/<int:pk>/', views.PaymentUpdateAPIView.as_view()),

]