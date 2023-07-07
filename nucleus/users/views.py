from django.shortcuts import render
from django.http import JsonResponse
from nucleus.users.models import UserPrefrenceModel
import json
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def save_prefrences_user(request):
    if request.method == 'POST':
        username=request.user.id
        path_model=request.POST.get("path_model",None)
        data=request.POST.get('updatedPrefrences')
        data=json.loads(data)
        try:

            obj=UserPrefrenceModel.objects.get(user=username,model_path=path_model)
            obj.json_data=data
            obj.save()
        except ObjectDoesNotExist:
            obj=UserPrefrenceModel(user=request.user,model_path=path_model,json_data=data)
            obj.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
    