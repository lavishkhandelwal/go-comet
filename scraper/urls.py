from .views import index, search, history, detail, deletehistory, api
from django.urls import path

urlpatterns = [
    path('', index, name = 'index'),
    path('search/', search, name = 'search'),
    path('history/', history, name = 'history'),
    path('detail/', detail, name = 'detail'),
    path('deletehistory/', deletehistory, name = 'deletehistory'),
    path('api/', api, name = "api"),
]