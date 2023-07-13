# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
from django.conf import settings
import os
from django.shortcuts import render, HttpResponse
import polib

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



def po_file_view(request):
    base_dir = settings.BASE_DIR
    language = Profile.objects.get(user=request.user).language
    po = polib.pofile(os.path.join(base_dir, 'locale', language, 'LC_MESSAGES', 'django.po'))
    print(type(po))
    if request.method == 'POST':
        if 'save' in request.POST:
            po_txt = request.POST.get('my_textarea')
            po_file_path = os.path.join(base_dir, 'locale', language, 'LC_MESSAGES', 'django.po')
            with open(po_file_path, 'w') as po_file:
                po_file.write(po_txt)
            os.system(f'python manage.py makemessages -l {language}')
            # return HttpResponse('File saved successfully')
            return redirect('/admin/')
            
    return render(request, 'admin/po_file_editor.html', {'po_file_full':po})

