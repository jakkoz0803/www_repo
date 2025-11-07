from posts.models import Category, Topic, Post
from posts.serializers import CategorySerializer, PostSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

# Tworzymy nową kategorię
cat = Category(name='Sport', description='Sport news')
cat.save()

# Serializator CategorySerializer
serializer = CategorySerializer(cat)
print(serializer.data)

# Konwersja do JSON
json_data = JSONRenderer().render(serializer.data)
print(json_data)

# Deserializacja
stream = io.BytesIO(json_data)
data = JSONParser().parse(stream)
deserializer = CategorySerializer(data=data)
print(deserializer.is_valid())
print(deserializer.validated_data)

# Serializator PostSerializer
post = Post(title='New football post', text='This is a test post', topic=None, slug='football-post', created_by_id=1)
post.save()
serializer_post = PostSerializer(post)
print(serializer_post.data)
