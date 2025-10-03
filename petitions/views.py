from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Petition, Vote
from .forms import PetitionForm, VoteForm

@login_required
def petition_list(request):
    petitions = Petition.objects.all().order_by('-created_at')
    return render(request, 'petitions/petition_list.html', {'petitions': petitions})

@login_required
def create_petition(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('petitions:list')
    else:
        form = PetitionForm()
    
    return render(request, 'petitions/create_petition.html', {'form': form})

@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    
    # Check if user already voted
    existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()
    
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote_type = form.cleaned_data['vote_type']
            
            if existing_vote:
                # Update existing vote
                existing_vote.vote_type = vote_type
                existing_vote.save()
                messages.success(request, 'Your vote has been updated!')
            else:
                # Create new vote
                vote = form.save(commit=False)
                vote.petition = petition
                vote.user = request.user
                vote.save()
                messages.success(request, 'Your vote has been recorded!')
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'yes_count': petition.yes_votes_count(),
                    'no_count': petition.no_votes_count()
                })
            
            return redirect('petitions:list')
    
    # For GET requests, show current vote status
    context = {
        'petition': petition,
        'user_vote': existing_vote.vote_type if existing_vote else None,
    }
    return render(request, 'petitions/petition_detail.html', context)