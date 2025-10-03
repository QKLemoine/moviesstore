from django import forms
from .models import Petition, Vote

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description', 'movie_title', 'release_year', 'director']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote_type']