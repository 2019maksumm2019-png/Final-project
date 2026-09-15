from django.urls import path
from .views import (
    RecipeListView, 
    RecipeDetailView, 
    RecipeCreateView, 
    RecipeUpdateView, 
    RecipeDeleteView, 
    RecipeLikeView
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/add/', RecipeCreateView.as_view(), name='recipe_add'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipe/<int:pk>/like/', RecipeLikeView.as_view(), name='recipe_like'),
]