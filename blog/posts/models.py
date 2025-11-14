from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Topic(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    slug = models.SlugField()
    created_at = models.DateTimeField(default=timezone.now)  # ✅ naprawione
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        """
        Walidacja pól:
        - title: tylko litery i spacje,
        - created_at: nie może być z przyszłości.
        """
        if not all(ch.isalpha() or ch.isspace() for ch in self.title):
            raise ValidationError({'title': "Tytuł może zawierać tylko litery i spacje."})

        if self.created_at and self.created_at > timezone.now():
            raise ValidationError({'created_at': "Data dodania nie może być z przyszłości."})

    def __str__(self):
        words = self.text.split()
        return ' '.join(words[:5]) + ('...' if len(words) > 5 else '')

    class Meta:
        ordering = ['-created_at']
