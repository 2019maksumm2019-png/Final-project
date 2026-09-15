from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'cooking_time', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control mb-3'})