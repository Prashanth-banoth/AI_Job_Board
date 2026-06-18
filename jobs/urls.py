from django.urls import path
from .views import job_list, apply_job, my_applications,submit_application,live_jobs,save_job,my_saved_jobs
urlpatterns = [
    path('', job_list),
    path('apply/<int:job_id>/', apply_job),
    path('my-applications/', my_applications),
    path('submit/<int:job_id>/<int:resume_id>/', submit_application),
    path('live-jobs/',live_jobs),
    path('save/<int:job_id>/',save_job),
    path('saved-jobs/',my_saved_jobs),


]
