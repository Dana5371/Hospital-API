from datetime import timedelta
from .parsing import main
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from main.models import Department
from .serializers import *
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from .permissions import IsHealthProblemAuthor


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    

class DoctorListlView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny, ]

    
class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, ]

    
class HealthProblemViewSet(ModelViewSet):
    queryset = HealthProblem.objects.all()
    serializer_class = HealthProblemSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        if self.action is ['update', 'partial_update', 'destroy']:
            permissions = [IsHealthProblemAuthor, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('day', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created__gte=start_date)
        return queryset


    @action(methods=['GET'], detail=False)
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = HealthProblemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(Q(title__icontains=query) | Q(description__icontains=query))
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        queryset = Favorite.objects.all()
        queryset = queryset.filter(user=request.user)
        serializer = FavoriteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        health_problem = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user, health_problem=health_problem)
        if not created:
            obj.favorite = not obj.favorite
            obj.save()
        favorites = 'added to favorites' if obj.favorite else 'removed to favorites'
        return Response('Successfully {} !'.format(favorites), status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

    
class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, ]

    
class LikesViewSet(ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated, ]


class ParsingView(APIView):
    def get(self, request):
        parsing = main()

        serializer = ParsingSerializer(instance=parsing, many=True)
        return Response(serializer.data)
