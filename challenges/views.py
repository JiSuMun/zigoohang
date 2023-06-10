from django.shortcuts import render, redirect
from .models import Challenge, ChallengeImage
from .forms import ChallengeForm, ChallengeImageForm, ChallengeImage_DeleteImageForm

# Create your views here.
def index(request):
    challenges = Challenge.objects.all()

    context = {
        'challenges': challenges
    }
    return render(request, 'challenges/index.html', context)


def detail(request, challenge_pk):
    challenge = Challenge.objects.get(pk=challenge_pk)
    challenge_images = ChallengeImage.objects.filter(challenge=challenge_pk)

    context = {
        'challenge': challenge,
        'challenge_images': challenge_images
    }

    return render(request, 'challenges/detail.html', context)


def create(request):
    Challenge_form = ChallengeForm()
    image_form = ChallengeImageForm()

    if request.method == 'POST':
        Challenge_form = ChallengeForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if Challenge_form.is_valid():
            challenge = Challenge_form.save(commit=False)
            challenge.creator = request.user
            challenge.end_date = '9999-09-09'
            challenge.start_date = '2023-06-16'
            challenge.save()
            for i in files:
                ChallengeImage.objects.create(image=i, challenge=challenge)
            return redirect('challenges:detail', challenge.pk)
    context = {
        'form': Challenge_form,
        'image_form': image_form,
    }
    
    return render(request, 'challenges/create.html', context)


def update(request, challenge_pk):
    challenge = Challenge.objects.get(pk=challenge_pk)
    print(challenge)
    if request.method == 'POST':
        print(2)
        challenge_form = ChallengeForm(request.POST, instance=challenge)
        files = request.FILES.getlist('image') 
        delete_ids = request.POST.getlist('delete_images')
        delete_image_form = ChallengeImage_DeleteImageForm(challenge=challenge, data=request.POST)

        if challenge_form.is_valid() and delete_image_form.is_valid():
            challenge = challenge_form.save(commit=False)
            challenge.user = request.user
            challenge.save()

            for delete_id in delete_ids: 
                challenge.challengeimage_set.filter(pk=delete_id).delete()

            for i in files: 
                ChallengeImage.objects.create(image=i, challenge=challenge)

            return redirect('challenges:detail', challenge.pk)
        
    else:
        challenge_form = ChallengeForm(instance=challenge)
        delete_image_form = ChallengeImage_DeleteImageForm(challenge=challenge)

    if challenge.challengeimage_set.exists():
        image_form = ChallengeImageForm(instance=challenge.challengeimage_set.first())

    else:
        image_form = ChallengeImageForm()

    context = {
        'challenge': challenge,
        'challenge_form': challenge_form,
        'image_form': image_form,
        'delete_image_form': delete_image_form,
    }

    return render(request, 'challenges/update.html', context)


def delete(request, challenge_pk):
    challenge = Challenge.objects.get(pk=challenge_pk)
    if request.user == challenge.creator:
        challenge.delete()
    return redirect('challenges:index')