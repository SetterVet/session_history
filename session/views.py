
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from .forms import UploadFileForm
from .models import CSVFile
import csv
import json


def index(request):
    if request.method == 'POST':

        try:
            file_from_html=request.FILES['file']
        except MultiValueDictKeyError:
            message="You don't input a file"
            return render(request, 'session/index.html',{'message':message})
        current_input_file = CSVFile(file=file_from_html,title=file_from_html.name)
        current_input_file.save()

        return HttpResponseRedirect('/result/'+str(current_input_file.pk))

    else:
        return render(request, 'session/index.html')

def calc(pk):
    f=CSVFile.objects.get(pk=pk)
    with open('session/reader.csv', 'wb+') as dest:
        for chunk in f.file.chunks():
            dest.write(chunk)

    with open('session/reader.csv', 'r') as csvfile:
        reader=csv.reader(csvfile)
        fields = [[] for _ in range(16)]
        i, j = 0, 0
        for row in reader:
            for item in row:
                if i != 0:
                    fields[j].append(item)
                    j += 1

            i += 1
            j = 0

    return fields

def result(request,pk):

    result=calc(pk)
    print(result)
    return render(request,'session/result.html')