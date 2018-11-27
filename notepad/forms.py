from django import forms

from .models import Note


class NoteModelForm(forms.ModelForm):
    class Meta:
        model = Note
        # following fields in a Note model will be inputted by user
        fields = ['title', 'url', 'image']
