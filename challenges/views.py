from django.shortcuts import render, redirect
from .models import Challenge, ChallengeImage, Certification
from .forms import ChallengeForm, ChallengeImageForm, ChallengeImage_DeleteImageForm, CertificationForm
from django.core.paginator import Paginator


def index(request):
    challenges = Challenge.objects.all().order_by('-created')
    paginator = Paginator(challenges, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj' : page_obj,
    }
    return render(request, 'challenges/index.html', context)


def detail(request, challenge_pk):
    challenge = Challenge.objects.get(pk=challenge_pk)
    challenge_images = ChallengeImage.objects.filter(challenge=challenge_pk)
    certification_form = CertificationForm() 
    certifications = challenge.certifications.all()
    
    u_certification_forms = []

    for certification in certifications:
        u_certification_form = (
            certification,
            CertificationForm(instance=certification),
            
        )
        u_certification_forms.append(u_certification_form)
        
    context = {
        'challenge': challenge,
        'challenge_images': challenge_images,
        'certification_form': certification_form,
        'u_certification_forms': u_certification_forms,
        'certifications': certifications
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


def certification_create(request, challenge_pk):
    challenge = Challenge.objects.get(pk=challenge_pk)

    if request.method == 'POST':
        certification_form = CertificationForm(request.POST, request.FILES)
        if certification_form.is_valid():
            certification = certification_form.save(commit=False)
            certification.user = request.user
            certification.challenge = challenge
            certification.save()
            return redirect('challenges:detail', challenge_pk)
    else:
        certification_form = CertificationForm()

    context = {
        'certification_form': certification_form,
        'challenge': challenge,
    }
    return render(request, 'challenges/detail.html', context)


def certification_update(request, challenge_pk, certification_pk):
    challenge = Challenge.objects.get(pk=challenge_pk)
    certification = Certification.objects.get(pk=certification_pk)
    u_certification_form = CertificationForm(instance=certification)
    
    if request.method == 'POST':
        u_certification_form = CertificationForm(request.POST, request.FILES, instance=certification)
        
        if u_certification_form.is_valid():
            certification = u_certification_form.save(commit=False)
            certification.challenge = challenge
            certification.user = request.user
            certification.save()

        return redirect('challenges:detail', challenge.pk)
    
    context = {
        'challenge': challenge,
        'certification': certification,
        'u_certification_form': u_certification_form,
    }
    return render(request, 'challenges/detail.html', context)



def certification_delete(request, challenge_pk, certification_pk):
    certification = Certification.objects.get(pk=certification_pk)
    if request.user == certification.user:
        certification.delete()

    return redirect('challenges:detail', challenge_pk)