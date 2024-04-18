from django.shortcuts import render
from rest_framework import generics
from  .models import Tikit
from .serializers import TikitSerializer
# Create your views here.


class TikitCreateAPIView(generics.CreateAPIView):
    queryset = Tikit.objects.all()
    serializer_class = TikitSerializer