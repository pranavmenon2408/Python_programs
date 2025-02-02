from django.shortcuts import render 
import json 
 
from .models import Location
 
def home(request):
    return render(request, 'base.html')
def index(request):
    location_list = list(Location.objects.order_by('name').values()) 
    location_json = json.dumps(location_list)  
    context = {'locations': location_json} 
    return render(request, 'map.html', context)