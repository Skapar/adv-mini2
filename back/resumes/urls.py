from django.urls import path
from .views import (
    ResumeUploadView, 
    ResumeDetailView, 
    JobDescriptionCreateView,
    JobDescriptionMatchView, 
    JobDescriptionListView, 
    JobDescriptionDetailView, 
    ResumeReplaceView
)

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('replace/', ResumeReplaceView.as_view(), name='resume-replace'),
    path('<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
    path('jobs/create/', JobDescriptionCreateView.as_view(), name='job-create'),
    path('jobs/<int:job_id>/matches/', JobDescriptionMatchView.as_view(), name='job-matches'),
    path('jobs/', JobDescriptionListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDescriptionDetailView.as_view(), name='job-detail'),
]