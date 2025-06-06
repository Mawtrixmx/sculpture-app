from django import forms
from .models import Sculpture

class SculptureUploadForm(forms.ModelForm):
    class Meta:
        model = Sculpture
        fields = ['image', 'price']
