from django.shortcuts import render
from .models import File
import csv
def index(request):
    if request.method=='POST':
        inpfile=request.POST['csv']
        File.create(inpfile)
    else:
        return render(request,'session/index.html')
