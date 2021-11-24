from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from main.models import Department
from .serializers import *
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
# Create your views here.
class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    

class DoctorListlView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class HealthProblemViewSet(ModelViewSet):
    queryset = HealthProblem.objects.all()
    serializer_class = HealthProblemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(Q(title__icontains=query) | Q(description__icontains=query))
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    