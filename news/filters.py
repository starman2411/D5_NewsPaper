from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['time_creation__gt'].label = 'Дата размещения позже чем:'
        self.filters['title__icontains'].label = 'Заголовок'
        self.filters['author__user__username__icontains'].label = 'Автор'


    class Meta:
        model = Post
        fields = {
            'time_creation': ['gt'],
            'title': ['icontains'],
            'author__user__username': ['icontains'],
        }

