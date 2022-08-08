from .models import Post, Author, Category, Comment
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import render
from django.views import View


class PostList(ListView):
    model = Post
    ordering = 'time_create'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    queryset = Post.objects.order_by('-time_create')
    form_class = PostForm
    paginate_by = 10 # вот так мы можем указать количество записей на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = PostForm
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — news_one.html
    template_name = 'news_one.html'
    # Название объекта, в котором будет выбранная пользователем новость
    context_object_name = 'news_one'


class HomePageView(View):
    template_name = "index.html"


class SearchNews(ListView):
    template_name = 'search.html'
    context_object_name = 'search_news'
    queryset = Post.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['form'] = PostForm
        return context

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = "/news/"

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
# Create your views here.
