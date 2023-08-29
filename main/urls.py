from django.urls import path
from . import views


urlpatterns = [
    path('home/' , views.home , name='home'),
    path('' , views.user_login , name="login"),
    path('segment/' , views.segment , name="segment"),
    path('signup/' , views.user_signup , name="signup"),
    path('audio/' , views.audio , name="audio"),
    path('table/' , views.table , name="table"),
    path('show/' , views.show_data , name="show"),
    path('logout/' , views.user_logout , name="logout"),
    path('update/<int:id>/' , views.update_content , name="update"),
    path('download_json/<int:id>/', views.download_json, name='download_json'),
    path('my_json/<int:id>/', views.my_json, name='my_json'),
    path('G_segment', views.Segmented_Text.as_view(), name='myapi'),
    path('N_G_segment', views.No_Segmented_Text.as_view(), name='mynewapi'),

]