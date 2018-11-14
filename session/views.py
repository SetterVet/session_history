from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from .forms import UploadFileForm
from .models import CSVFile
import csv
import json


def index(request):
    if request.method == 'POST':

        try:
            file_from_html = request.FILES['file']
        except MultiValueDictKeyError:
            message = "You don't input a file"
            return render(request, 'session/index.html', {'message': message})
        current_input_file = CSVFile(file=file_from_html, title=file_from_html.name)
        current_input_file.save()

        return HttpResponseRedirect('/result/' + str(current_input_file.pk))

    else:
        return render(request, 'session/index.html')


def calc(pk):
    f = CSVFile.objects.get(pk=pk)
    with open('session/reader.csv', 'wb+') as dest:
        for chunk in f.file.chunks():
            dest.write(chunk)

    with open('session/reader.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
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


def pass_vs_error_date(result):
    summary_status = result[3]
    created_at = result[2]

    for i in range(len(created_at)):
        created_at[i] = datetime.strptime(created_at[i], '%Y-%m-%d %H:%M:%S %Z')
        created_at[i] = created_at[i].strftime('%Y-%m-%d')  # datetime.date(datetime.strptime(created_at[i], '%Y-%m-%d %H:%M:%S %Z'))
        created_at[i] = datetime.strptime(created_at[i], '%Y-%m-%d')
        created_at[i] = created_at[i].timestamp()
    dates, passed, error = list(), list(), list()
    for item in created_at:
        if item not in dates:
            dates.append(item)
            passed.append(0)
            error.append(0)
    for i in range(len(summary_status)):
        if summary_status[i] == 'passed':
            passed[dates.index(created_at[i])] += 1
        else:
            error[dates.index(created_at[i])] += 1
    return [dates, passed, error]


def result(request, pk):
    calculate = calc(pk)

    plot1_data = pass_vs_error_date(calculate)
    return render(request, 'session/result.html', {'unique_dates': plot1_data[0], 'passed': plot1_data[1], 'error':
        plot1_data[2]})
