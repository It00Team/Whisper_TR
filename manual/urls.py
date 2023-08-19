
from django.urls import path , include
from .views import *
from . import views

urlpatterns = [
    path('segment/', my_function, name='manual_segment'),
    path('segments/', views.manseg.as_view(), name='man_segment'),
    path('final/', views.finaldata.as_view(), name='final_data'),
    path('jsondata/', views.CreateJsonFileView.as_view(), name='json_data'),

]