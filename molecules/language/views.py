# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
from django.conf import settings
import os

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

import polib

# views.py
import polib
from django.shortcuts import render
from django.http import HttpResponse

# def po_file_view(request):
#     print(request.method)
    
#     if request.method == 'POST' and request.FILES.get('po_file'):
#         print(request.method , "inside foor loop")
#         po_file = request.FILES['po_file'].read().decode('utf-8')
#         po = polib.pofile(po_file)

#         return render(request, 'admin/po_file_editor.html', {'po': po})

#     elif request.method == 'POST':
#         po_file = request.FILES['po_file'].read().decode('utf-8')
        
#         po = polib.pofile(po_file)
#         po.save()

#         if request.POST.get('save'):
#             # Update the PO file with the edited values
#             for entry in po:
#                 msgid = request.POST.get(f'msgid_{entry.msgid}')
#                 msgstr = request.POST.get(f'msgstr_{entry.msgid}')
#                 entry.msgid = msgid
#                 entry.msgstr = msgstr

#             # Save the updated PO file
#             po.save()

#         print("inside save")
#         print(po)

#         return HttpResponse('File saved successfully')
#     return render(request, 'admin/po_file_upload.html')
    


# views.py
from django.shortcuts import render, HttpResponse
import polib



def po_file_view(request):
    base_dir = settings.BASE_DIR
    lenguages =[]
    for laguage_dir in os.listdir(os.path.join(base_dir, 'locale')):
        if os.path.isdir(os.path.join(base_dir, 'locale', laguage_dir)):
            lenguages.append(laguage_dir)
    if request.method == 'POST':
        if 'po_file' in request.FILES:
            po_file = request.FILES['po_file'].read().decode('utf-8')
            print(request.FILES['po_file'])
            po = polib.pofile(po_file)
            lenguages = lenguages
            return render(request, 'admin/po_file_editor.html', {'po': po, 'lenguages': lenguages})
        if 'save' in request.POST:
            if not request.POST.get('lenguage'):
                language = Profile.objects.get(user=request.user).language
            language = request.POST.get('lenguage')
            print(language)
            po = polib.pofile(os.path.join(base_dir, 'locale', language, 'LC_MESSAGES', 'django.po'))
            # print(po)
            for entry in po:
                # print(entry.msgstr)
                msgid = request.POST.get(f'msgid_{entry.msgid}')
                msgstr = request.POST.get(f'msgstr_{entry.msgstr}')
                if (msgstr is None or msgstr == "") or (entry.msgstr is None):
                    msgstr = msgid
                    entry.msgstr = msgstr
                    print(msgstr," is none", msgid)
                entry.msgid = msgid
                entry.msgstr = msgstr
                # print(entry.msgid)
                print(entry.msgstr)

            entries = po.translated_entries()
            entries.sort(key=lambda o: (o.msgid_with_context or '').encode('utf-8'))
            po.save_as_mofile(os.path.join(base_dir, 'locale', language, 'LC_MESSAGES', 'django.mo'))
            po.save()
            os.system(f'python manage.py makemessages -l {language}')
            
    return render(request, 'admin/po_file_upload.html')

