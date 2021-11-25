from django.db.models import fields
from rest_framework import serializers
from .models import *


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = RatingSerializer(instance.rating, many=True).data
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
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    
    class Meta:
        model = HealthProblem
        exclude = ('author',)


    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        problem = HealthProblem.objects.create(**validated_data)
        return problem

    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     images_data = request.FILES
    #     instance.image.all().delete()
    #     return instance


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        # representation['likes'] = LikesSerializer(instance.likes.all(), many=True).data
        action = self.context.get('action')
        if action == 'list':
            representation['answer'] = instance.answer.count()
        else:
            representation['answer'] = AnswerSerializer(instance.answer.all(), many=True).data
        return representation



class AnswerSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Answer
        exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        problem = Answer.objects.create(**validated_data)
        return problem


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['author'] = instance.author.email
        return representation

class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Comment
        exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        problem = Comment.objects.create(**validated_data)
        return problem


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        return representation





class RatingSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        doctor = validated_data.get('doctor')
        print(validated_data)
        rating = Rating.objects.get_or_create(author=author, doctor=doctor)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating
    

# class LikesSerializer(serializers.ModelSerializer):
#
#
#     class Meta:
#         model = Likes
#          exclude = ('author',)
#
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user_id = request.user.id
#         validated_data['author_id'] = user_id
#         problem = HealthProblem.objects.create(**validated_data)
#         return problem
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['author'] = instance.author.email
#         return representation

   
  




 


            

