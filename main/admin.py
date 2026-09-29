from django.contrib import admin
from .models import Recipe, RecipeStep, Comment

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'cooking_time', 'author', 'created_at')
    inlines = [RecipeStepInline]

admin.site.register(Comment)