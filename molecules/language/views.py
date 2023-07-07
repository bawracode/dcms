# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile

@login_required
def language_selection_view(request):
    if request.method == 'POST':
        language = request.POST.get('language')  # Assuming language selection is provided in the request data
        profile = Profile.objects.get(user=request.user)
        profile.language = language
        profile.save()
        return redirect('admin')  # Redirect to the admin site or any other desired page
    else:
        return render(request, 'language_selection.html')
