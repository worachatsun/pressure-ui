from django.urls import path
from preassure_management.views import Record, StopRecord
from preassure_management import views

urlpatterns = [
    path('', views.index, name='index'),
    path('record', Record.as_view(), name='record'),
    path('stopRecord', StopRecord.as_view(), name='stopRecord'),
]
