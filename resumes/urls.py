from django.urls import path
from .views import upload_resume, my_resumes
from .views import upload_resume, my_resumes, analyze_resume, ai_resume_feedback

urlpatterns = [
    path('upload/<int:job_id>/', upload_resume),
    path('my-resumes/', my_resumes),
    path('analyze/<int:job_id>/', analyze_resume),
    path('ai-feedback/<int:job_id>/',ai_resume_feedback),
    
]