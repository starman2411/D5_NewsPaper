from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
# Create your views here.
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-time_creation']
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsListFiltered(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'filtered_posts'
    ordering = ['-time_creation']
    paginate_by = 10

    filterset_class = PostFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'add.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'