from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from time import sleep
import os, signal, subprocess, serial, glob
from preassure_management import script
import pyrebase

def index(request):
    list_of_files = glob.glob('data/pressure/*.csv')
    file_name = script.getFileName()
    os.system("TASKKILL /F /IM pythonw.exe")
    context = {
        "transcript": script.tran[file_name],
        "phoneme": script.tran_phone[file_name],
        "new_file_name": file_name,
        "list_of_files": [file.split("\\")[1] for file in list_of_files][::-1][:5],
        "files_length": len(list_of_files)
    }
    return render(request, 'index.html', context)

class Record(View):
    def post(self, request):
        file_name = script.getFileName()
        command = 'pythonw C:/Users/Sun/Desktop/works/pressure-ui/arduino/pressure.py ' + file_name
        subprocess.Popen(command)
        list_of_files = glob.glob('data/pressure/*.csv')
        context = {
            "transcript": script.tran[file_name],
            "phoneme": script.tran_phone[file_name],
            "new_file_name": file_name,
            "list_of_files": [file.split("\\")[1] for file in list_of_files][::-1][:5],
            "files_length": len(list_of_files),
            "record": True
        }
        return render(request, 'index.html', context)

class RecordJSON(View):
    def post(self, request):
        file_name = request.body.decode('utf-8')
        # print(body_unicode)
        # file_name = script.getFileName()
        # print(file_name)
        command = 'pythonw C:/Users/Sun/Desktop/works/pressure-ui/arduino/pressure.py ' + file_name
        subprocess.Popen(command)
        list_of_files = glob.glob('data/pressure/*.csv')
        data = {
            "transcript": script.tran[file_name],
            "phoneme": script.tran_phone[file_name],
            "new_file_name": file_name,
            "list_of_files": [file.split("\\")[1] for file in list_of_files][::-1][:5],
            "files_length": len(list_of_files),
            "record": True
        }
        return JsonResponse(data, safe=False)

class getTargetJSON(View):
    def post(self, request):
        file_name = request.body.decode('utf-8')
        data = {
            "transcript": script.tran[file_name],
            "phoneme": script.tran_phone[file_name],
            "new_file_name": file_name
        }
        return JsonResponse(data, safe=False)

class StopRecordJSON(View):
    def post(self, request):
        os.system("TASKKILL /F /IM pythonw.exe")
        file_name_cur = request.body.decode('utf-8')
        self.firebaseUpload(file_name_cur)
        file_name = script.getFileName()
        list_of_files = glob.glob('data/pressure/*.csv')
        data = {
            "transcript": script.tran[file_name],
            "phoneme": script.tran_phone[file_name],
            "new_file_name": file_name,
            "list_of_files": [file.split("\\")[1] for file in list_of_files][::-1][:5],
            "files_length": len(list_of_files),
            "record": True
        }
        return JsonResponse(data, safe=False)

    def firebaseUpload(self, file_name_cur):
        config = {
            "config": 'xxx'
        }

        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        path_on_cloud = "csv/"+file_name_cur+".csv"
        path_local = "C:/Users/Sun/Desktop/works/pressure-ui/pressure-ui/preassure/data/pressure/"+file_name_cur+".csv"
        storage.child(path_on_cloud).put(path_local)
        
class StopRecord(View):
    def post(self, request):
        os.system("TASKKILL /F /IM pythonw.exe")
        return redirect('/')

class SensorContent(View):
    def get(self, request, file_name):
        try:
            lines = self.tail("C:/Users/Sun/Desktop/works/pressure-ui/pressure-ui/preassure/data/pressure/"+file_name+".csv", 10)
            data = [[], []]
            for line in lines:
                data[0].append(line.split(',')[0])
                data[1].append(line.split(',')[1][1:-1])
        except:
            data = None
        return JsonResponse(data, safe=False)

    def tail(self, file, n=1, bs=1024):
        f = open(file)
        f.seek(0,2)
        l = 1-f.read(1).count('\n')
        B = f.tell()
        while n >= l and B > 0:
            block = min(bs, B)
            B -= block
            f.seek(B, 0)
            l += f.read(block).count('\n')
        f.seek(B, 0)
        l = min(l,n)
        lines = f.readlines()[-l:]
        f.close()
        return lines