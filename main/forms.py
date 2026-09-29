from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'difficulty', 'description', 'ingredients', 'cooking_time', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Коротко розкажіть про страву...'}),
            'ingredients': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Наприклад:\n- Борошно 200г\n- Яйця 2шт'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control mb-3'})