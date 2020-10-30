from django.urls import path
from preassure_management.views import Record, StopRecord, SensorContent, RecordJSON, StopRecordJSON
from preassure_management import views

urlpatterns = [
    path('', views.index, name='index'),
    path('record', Record.as_view(), name='record'),
    path('recordJSON', RecordJSON.as_view(), name='recordJSON'),
    path('stopRecordJSON', StopRecordJSON.as_view(), name='stopRecordJSON'),
    path('stopRecord', StopRecord.as_view(), name='stopRecord'),
    path('sensorContent/<str:file_name>', SensorContent.as_view(), name='sensorContent'),
]
