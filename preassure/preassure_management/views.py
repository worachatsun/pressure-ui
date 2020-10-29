from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from time import sleep
import os, signal, subprocess, serial, glob
from preassure_management import script

def index(request):
    list_of_files = glob.glob('data/pressure/*.csv')
    file_name = script.getFileName()
    context = {
        "new_file_name": file_name,
        "list_of_files": [file.split("\\")[1] for file in list_of_files][::-1][:10],
        "files_length": len(list_of_files)
    }
    return render(request, 'index.html', context)

class Record(View):
    def post(self, request):
        list_of_files = glob.glob('data/pressure/*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file_name = str(int(latest_file.split("\\")[1].split(".")[0])+1)
        command = 'pythonw C:/Users/Sun/Desktop/works/pressure-ui/arduino/pressure.py ' + latest_file_name
        subprocess.Popen(command)
        return redirect('/')

class StopRecord(View):
    def post(self, request):
        os.system("TASKKILL /F /IM pythonw.exe")
        return redirect('/')