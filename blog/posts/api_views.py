from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSerializer


# === CATEGORY ===
@api_view(['GET', 'POST'])
def category_list(request):
    """Lista wszystkich kategorii lub dodanie nowej"""
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def category_detail(request, pk):
    """Wyświetlenie lub usunięcie pojedynczej kategorii"""
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def category_search(request):
    """Wyszukiwanie kategorii po fragmencie nazwy"""
    query = request.query_params.get('q', '')
    categories = Category.objects.filter(name__icontains=query)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# === TOPIC ===
@api_view(['GET', 'POST'])
def topic_list(request):
    """Lista wszystkich tematów lub dodanie nowego"""
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def topic_detail(request, pk):
    """Wyświetlenie lub usunięcie pojedynczego tematu"""
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def topic_search(request):
    """Wyszukiwanie tematów po fragmencie nazwy"""
    query = request.query_params.get('q', '')
    topics = Topic.objects.filter(name__icontains=query)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


# === POST ===
@api_view(['GET', 'POST'])
def post_list(request):
    """Lista wszystkich postów lub dodanie nowego"""
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    """Wyświetlenie, aktualizacja lub usunięcie pojedynczego posta"""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def post_search(request):
    """Wyszukiwanie postów po tytule zawierającym podany fragment"""
    query = request.query_params.get('q', '')
    posts = Post.objects.filter(title__icontains=query)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
