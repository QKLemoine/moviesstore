from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    movie_title = models.CharField(max_length=200)
    release_year = models.IntegerField(blank=True, null=True)
    director = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def yes_votes_count(self):
        return self.votes.filter(vote_type='yes').count()
    
    def no_votes_count(self):
        return self.votes.filter(vote_type='no').count()

class Vote(models.Model):
    VOTE_TYPES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=3, choices=VOTE_TYPES)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['petition', 'user']