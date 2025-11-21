from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSerializer

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'DELETE'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=204)

@api_view(['GET'])
def category_search(request):
    query = request.query_params.get('q', '')
    categories = Category.objects.filter(name__icontains=query)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def topic_list(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'DELETE'])
def topic_detail(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        topic.delete()
        return Response(status=204)

@api_view(['GET'])
def topic_search(request):
    query = request.query_params.get('q', '')
    topics = Topic.objects.filter(name__icontains=query)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])     # POST wymaga logowania
@authentication_classes([TokenAuthentication])
def post_list(request):
    """GET list, POST create post"""

    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # <== KLUCZOWA LINIJKA
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT'])
def post_detail(request, pk):
    """GET or UPDATE post"""

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=404)

    post.delete()
    return Response(status=204)

@api_view(['GET'])
def post_search(request):
    query = request.query_params.get('q', '')
    posts = Post.objects.filter(title__icontains=query)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_posts(request):
    posts = Post.objects.filter(created_by=request.user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_topics(request, pk):
    """Zwraca wszystkie Topic przypisane do danej kategorii (tylko odczyt, tylko token)."""
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    topics = Topic.objects.filter(category=category)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)
