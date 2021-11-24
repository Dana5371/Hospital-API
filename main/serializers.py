from django.db.models import fields
from rest_framework import serializers
from .models import *


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            representation['health_problem'] = instance.health.count()
        else:
            representation['health_problem'] = HealthProblemSerializer(instance.health.all(), many=True).data
        return representation



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

   

class HealthProblemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    
    class Meta:
        model = HealthProblem
        exclude = ('author', )


    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        problem = HealthProblem.objects.create(author=author, **validated_data)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.image.all().delete()
        return instance

        
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        action = self.context.get('action')
        if action == 'list':
            representation['answer'] = instance.answer.count()
        else:
            representation['answer'] = AnswerSerializer(instance.answer.all(), many=True).data
        return representation



class AnswerSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Answer
        fields = '__all__'

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     answer = Answer.objects.create(author=request.user, **validated_data)
    #     return answer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     comment = Comment.objects.create(author=request.user, **validated_data)
    #     return comment

    



   
  




 


            

