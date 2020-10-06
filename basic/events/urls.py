from django.conf.urls import url,include
from django.urls import path
from rest_framework import routers
from .views import EventCreateListView, EventUpdateDeleteView, \
    FileUploadView, FileOnlyUploadView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = 'events'
urlpatterns = [
    path('',EventCreateListView.as_view(),name='EventView'),
    path('<int:id>/',EventUpdateDeleteView.as_view(),name='EventUpdateDeleteView'),
    path('fileupload/',FileUploadView.as_view(),name='FileUpload'),
    path('fileonlyupload/',FileOnlyUploadView.as_view(),name='FileOnlyUpload'),
]