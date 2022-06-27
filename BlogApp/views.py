from django.shortcuts import render, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Posts, Category
from .forms import PostForm, EditForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Create your views here.

def LikeView(request, pk):
    # post = get_list_or_404(Post, id=request.POST.get('post_id'))
    post = Posts.objects.get(id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse_lazy('post_detail', args=[str(pk)]))


class HomeView(ListView):
    model=Posts
    template_name='home.html'
    ordering=['-post_date']
    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class PostDetailView(DetailView):
    model=Posts
    template_name='post_detail.html'
    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        
        stuff =  Posts.objects.get(id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["liked"] = liked
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        return context
def CategoryView(request, cats):
    category_posts=Posts.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts': category_posts })

class PostCreateView(CreateView):
    model=Posts
    form_class = PostForm
    template_name='post_new.html'
    # fields="__all__"
    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context
class CategoryCreateView(CreateView):
    model=Category
    template_name='category_new.html'
    fields="__all__"
    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(CategoryCreateView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context
class PostUpdateView(UpdateView):
    model=Posts
    template_name='update_post.html'
    form_class = EditForm
    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostUpdateView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context
class PostDeleteView(DeleteView):
    model=Posts
    template_name='delete_post.html'
    success_url = reverse_lazy('home')
    def get_context_data(self,*args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDeleteView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context








