from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    # Додаємо окреме поле для введення кроків текстом
    steps_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5, 
            'placeholder': '1. Підготувати інгредієнти...\n2. Змішати все у мисці...\n3. Випікати 20 хвилин...'
        }),
        label="Кроки приготування (кожен з нового рядка)",
        required=True
    )

    class Meta:
        model = Recipe
        fields = ['title', 'category', 'difficulty', 'description', 'ingredients', 'cooking_time', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Коротко розкажіть про страву...'}),
            'ingredients': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Наприклад:\nБорошно 200г\nЯйця 2шт'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control mb-3'})