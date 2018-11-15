from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from .forms import UploadFileForm
from .models import CSVFile
import csv
import json
import jsonify

def index(request):
    updated_files = CSVFile.objects.all()
    if request.method == 'POST':

        try:
            file_from_html = request.FILES['file']
        except MultiValueDictKeyError:
            message = "You don't input a file"
            return render(request, 'session/index.html', {'message': message,'files':updated_files})
        current_input_file = CSVFile(file=file_from_html, title=file_from_html.name)
        current_input_file.save()

        return HttpResponseRedirect('/result/' + str(current_input_file.pk))

    else:

        return render(request, 'session/index.html',{'files':updated_files})


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

    summary_status = result[3][:]
    created_at = result[2][:]

    for i in range(len(created_at)):
        created_at[i] = datetime.strptime(created_at[i], '%Y-%m-%d %H:%M:%S %Z')
        created_at[i] = created_at[i].strftime('%Y-%m-%d')  # datetime.date(datetime.strptime(created_at[i], '%Y-%m-%d %H:%M:%S %Z'))

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

def duration_vs_created_at(result):
    created_at = result[2][:]
    duration = result[4][:]
    for i in range(len(created_at)):
        created_at[i] = datetime.strptime(created_at[i], '%Y-%m-%d %H:%M:%S %Z')
        created_at[i] = created_at[i].strftime('%Y-%m-%d %H:%M:%S %Z')
    return [created_at,duration]

def result(request, pk):
    calculate = calc(pk)

    plot1_data = pass_vs_error_date(calculate)
    bad_day,error_bad_day=list(),list()
    dates=plot1_data[0][:]
    errors=plot1_data[2][:]
    for i in range(len(dates)):
        if errors[i]>=3:
            bad_day.append(dates[i])
            error_bad_day.append(errors[i])

    plot2_data=duration_vs_created_at(calculate)
    response = json.dumps({'unique_dates': dates,'passed': plot1_data[1] , 'error': errors
                           ,'bad_day':bad_day,'error_bad_day':error_bad_day,'created_at':plot2_data[0],
                           'duration':plot2_data[1]})

    return render(request, 'session/result.html', {'response': response})

def handler404(request):
    return render(request, 'session/page404.html', status=404)
