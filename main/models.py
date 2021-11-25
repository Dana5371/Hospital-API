from functools import update_wrapper
from django.db import models
from django.db.models.fields.files import ImageField
from account.models import User

# Create your models here.
class Department(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    image = models.ImageField(upload_to='doctors')
    name = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100, unique=True)
    experience = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return f"{self.name} {self.last_name}"

class HealthProblem(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='health')
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='healthproblems', blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    health_problem = models.ForeignKey(HealthProblem, on_delete=models.CASCADE, related_name='answer')
    answer = models.TextField()
    image = models.ImageField(upload_to='answer', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer')
    created= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.answer[:20]}'

class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment

class Rating(models.Model):
    rating = models.IntegerField(default=0)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return str(self.rating)

class Likes(models.Model):
    likes = models.BooleanField(default=False)
    health_problem = models.ForeignKey(HealthProblem, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return str(self.likes)

class Favorite(models.Model):
    health_problem = models.ForeignKey(HealthProblem, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    favorite = models.BooleanField(default=True)