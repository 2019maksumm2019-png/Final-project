from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

CATEGORY_CHOICES = [
    ('breakfast', 'Сніданки'),
    ('lunch', 'Обіди'),
    ('dinner', 'Вечері'),
    ('dessert', 'Десерти'),
    ('drinks', 'Напої'),
]

DIFFICULTY_CHOICES = [
    ('easy', 'Легко'),
    ('medium', 'Середньо'),
    ('hard', 'Складно'),
]

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва рецепта")
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='lunch', 
        verbose_name="Категорія"
    )
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='easy', 
        verbose_name="Складність"
    )
    description = models.TextField(verbose_name="Короткий опис")
    ingredients = models.TextField(verbose_name="Інгредієнти (кожен з нового рядка)")
    cooking_time = models.PositiveIntegerField(
        help_text="Час у хвилинах", 
        verbose_name="Час приготування"
    )
    image = models.ImageField(
        upload_to="recipes/", 
        blank=True, 
        null=True, 
        verbose_name="Головне зображення страви"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="recipes", 
        verbose_name="Автор"
    )
    likes = models.ManyToManyField(
        User, 
        related_name='liked_recipes', 
        blank=True, 
        verbose_name="Вподобайки"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепти"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    def total_likes(self):
        return self.likes.count()


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField(verbose_name="Номер кроку")
    description = models.TextField(verbose_name="Опис кроку")
    image = models.ImageField(upload_to="recipe_steps/", blank=True, null=True, verbose_name="Фото кроку")

    class Meta:
        verbose_name = "Крок приготування"
        verbose_name_plural = "Кроки приготування"
        ordering = ['step_number']

    def __str__(self):
        return f"{self.recipe.title} - Крок {self.step_number}"


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} - {self.recipe.title}'