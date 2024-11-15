from django.urls import path
from myapp.views import upload_to_s3

urlpatterns = [
    path('upload/', upload_to_s3, name='upload'),
]
