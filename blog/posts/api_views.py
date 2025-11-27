from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSerializer


# ============================
# === CATEGORY ENDPOINTS ===
# ============================

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


# Zadanie 5 (topics for category)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def category_topics(request, pk):
    """Lista wszystkich topiców dla wybranej kategorii — tylko dla zalogowanych"""
    try:
        topics = Topic.objects.filter(category_id=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


# ============================
# === TOPIC ENDPOINTS ===
# ============================

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def topic_detail(request, pk):
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
    query = request.query_params.get('q', '')
    topics = Topic.objects.filter(name__icontains=query)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


# ============================
# === POST ENDPOINTS ===
# ============================

@api_view(['GET', 'POST'])
def post_list(request):
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
    """Wyświetlenie, edycja i usunięcie posta z pełną kontrolą uprawnień"""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # === GET ===
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # === PUT (edycja) ===
    elif request.method == 'PUT':
        # Zadanie 3 — sprawdzamy, czy user może edytować cudzy post
        user = request.user

        if user != post.created_by and not user.has_perm('posts.can_edit_others_posts'):
            return Response(
                {"detail": "Brak uprawnień do edytowania cudzych postów."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # === DELETE (tylko z tokenem) ===
    elif request.method == 'DELETE':
        if not request.auth:
            return Response({"detail": "Brak tokena."}, status=status.HTTP_401_UNAUTHORIZED)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def post_search(request):
    query = request.query_params.get('q', '')
    posts = Post.objects.filter(title__icontains=query)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


# ============================
# === USER POST ENDPOINT ===
# ============================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request):
    """Zwraca posty zalogowanego użytkownika"""
    posts = Post.objects.filter(created_by=request.user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
