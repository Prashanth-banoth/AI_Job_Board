from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Job, Application, SavedJob
from resumes.models import Resume
import requests
import PyPDF2
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse


@login_required

def job_list(request):

    jobs = Job.objects.all()
    print("Total Jobs:", Job.objects.count())

    search = request.GET.get('search')
    location = request.GET.get('location')

    if search:
        jobs = jobs.filter(
            title__icontains=search
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    for job in jobs:
        job.user_resume = Resume.objects.filter(
            user=request.user,
            job=job
        ).last()

    applied_jobs = Application.objects.filter(
        user=request.user
    ).values_list(
        'job_id',
        flat=True
    )

    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).values_list(
        'job_id',
        flat=True
    )

    return render(
        request,
        'job_list.html',
        {
            'jobs': jobs,
            'applied_jobs': applied_jobs,
            'saved_jobs': saved_jobs
        }
    )


@login_required
def apply_job(request, job_id):

    job = Job.objects.get(id=job_id)

    resume = Resume.objects.filter(
        user=request.user,
        job=job
    ).last()

    if not resume:
        return redirect(
            '/resume/upload/' + str(job.id) + '/'
        )

    pdf_file = open(
        resume.resume_file.path,
        'rb'
    )

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    skills = job.required_skills.split(',')

    found_skills = []

    for skill in skills:

        if skill.strip().lower() in text.lower():
            found_skills.append(
                skill.strip()
            )

    ats_score = int(
        (len(found_skills) / len(skills)) * 100
    )

    Application.objects.get_or_create(
        user=request.user,
        job=job,
        defaults={
            'resume': resume,
            'ats_score': ats_score
        }
    )

    return redirect('/jobs/')


def my_applications(request):

    applications = Application.objects.filter(
        user=request.user
    )

    return render(
        request,
        'my_applications.html',
        {
            'applications': applications
        }
    )


def submit_application(request, job_id, resume_id):

    job = Job.objects.get(id=job_id)

    resume = Resume.objects.get(id=resume_id)

    job_skills = job.required_skills.split(',')

    pdf_file = open(
        resume.resume_file.path,
        'rb'
    )

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    matched = 0

    for skill in job_skills:

        if skill.strip().lower() in text.lower():
            matched += 1

    ats_score = int(
        (matched / len(job_skills)) * 100
    )

    Application.objects.update_or_create(
        user=request.user,
        job=job,
        defaults={
            'resume': resume,
            'ats_score': ats_score
        }
    )

    return redirect('/jobs/my-applications/')


def live_jobs(request):

    url = "https://www.arbeitnow.com/api/job-board-api"

    response = requests.get(url)

    data = response.json()

    jobs = data['data']

    return render(
        request,
        'live_jobs.html',
        {
            'jobs': jobs
        }
    )

def save_job(request, job_id):

    job = Job.objects.get(id=job_id)

    SavedJob.objects.get_or_create(
        user=request.user,
        job=job
    )

    return redirect('/jobs/')

def my_saved_jobs(request):

    saved_jobs = SavedJob.objects.filter(
        user=request.user
    )

    return render(
        request,
        'my_saved_jobs.html',
        {
            'saved_jobs': saved_jobs
        }
    )




def create_sample_jobs(request):
    Job.objects.create(
        title="Python Backend Developer",
        company="Infosys",
        location="Hyderabad",
        description="Develop backend APIs using Django.",
        required_skills="Python, Django, SQL",
        experience="Fresher",
        salary="6 LPA"
    )

    Job.objects.create(
        title="Frontend Developer",
        company="TCS",
        location="Bangalore",
        description="Build responsive web applications.",
        required_skills="HTML, CSS, JavaScript, React",
        experience="Fresher",
        salary="5 LPA"
    )

    Job.objects.create(
        title="Full Stack Developer",
        company="Wipro",
        location="Pune",
        description="Work on frontend and backend systems.",
        required_skills="Python, Django, React, PostgreSQL",
        experience="Fresher",
        salary="7 LPA"
    )

    return HttpResponse("Jobs Created Successfully")