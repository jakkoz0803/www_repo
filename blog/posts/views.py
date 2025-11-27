from django.shortcuts import render

# Create your views here.

# blog/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Category
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


class PostList(APIView):
    """
    GET — lista postów
    POST — dodanie nowego posta
    """
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    """
    GET — pojedynczy post
    PUT — modyfikacja
    DELETE — usunięcie
    """
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def category_secure_detail(request, pk):
    if not request.user.has_perm('posts.view_category'):
        raise PermissionDenied("Brak uprawnień do przeglądania kategorii")

    try:
        cat = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse("Kategoria nie istnieje")

    return HttpResponse(f"Kategoria: {cat.name}")