from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.db import models

from .models import Recipe, Comment
from .forms import RecipeForm

class RecipeListView(ListView):
    model = Recipe
    template_name = 'main/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort')

        if query:
            queryset = queryset.filter(title__icontains=query)
        if category:
            queryset = queryset.filter(category=category)

        if sort == 'time_asc':
            queryset = queryset.order_by('cooking_time')
        elif sort == 'likes_desc':
            queryset = queryset.annotate(likes_count=models.Count('likes')).order_by('-likes_count')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'main/recipe_detail.html'
    context_object_name = 'recipe'

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.user.is_authenticated:
            comment_text = request.POST.get('comment_text')
            if comment_text:
                Comment.objects.create(
                    recipe=recipe,
                    author=request.user,
                    text=comment_text
                )
        return redirect('recipe_detail', pk=recipe.pk)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'main/recipe_form.html'
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'main/recipe_form.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'main/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class RecipeLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)
        return redirect('recipe_detail', pk=pk)