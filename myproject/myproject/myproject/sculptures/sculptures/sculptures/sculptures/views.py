from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SculptureUploadForm
from .models import Sculpture
from animal_sculpture_classifier import AnimalSculptureClassifier
import os
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('upload')
    else:
        form = UserCreationForm()
    return render(request, 'sculptures/register.html', {'form': form})

@login_required
def upload_sculpture(request):
    classifier = AnimalSculptureClassifier(model_path=os.path.join(settings.BASE_DIR, 'model.joblib'))
    if request.method == 'POST':
        form = SculptureUploadForm(request.POST, request.FILES)
        if form.is_valid():
            sculpture = form.save(commit=False)
            sculpture.user = request.user
            image_path = os.path.join(settings.MEDIA_ROOT, sculpture.image.name)
            animal_type = classifier.predict(image_path)
            if animal_type:
                sculpture.animal_type = animal_type
                unique_code = classifier.store_sculpture_data(image_path, animal_type, sculpture.price)
                sculpture.unique_code = unique_code
                sculpture.save()
                return redirect('gallery')
    else:
        form = SculptureUploadForm()
    return render(request, 'sculptures/upload.html', {'form': form})

@login_required
def gallery(request):
    sculptures = Sculpture.objects.filter(user=request.user)
    return render(request, 'sculptures/gallery.html', {'sculptures': sculptures})
