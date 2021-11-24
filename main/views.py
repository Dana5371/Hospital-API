from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.views import APIView

from main.models import Department
from .serializers import *

# Create your views here.
class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    