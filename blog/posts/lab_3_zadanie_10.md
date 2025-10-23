from posts.models import Category, Topic, Post

Category.objects.all()

Category.objects.get(id=3)

Category.objects.filter(name__startswith='C')

Post.objects.order_by('-title').values_list('title', flat=True)

new_cat = Category(name='Nowa kategoria', description='Opis nowej kategorii')

new_cat.save()


