import PyPDF2
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Resume
from jobs.models import Job
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)



def upload_resume(request, job_id):

    job = Job.objects.get(id=job_id)

    if request.method == "POST":

        resume_file = request.FILES.get('resume')

        if resume_file:
            Resume.objects.create(
                user=request.user,
                job=job,
                resume_file=resume_file
            )

            return redirect('/jobs/')

    return render(
        request,
        'upload_resume.html',
        {'job': job}
    )

def my_resumes(request):

    resumes = Resume.objects.filter(user=request.user)

    return render(
        request,
        'my_resumes.html',
        {'resumes': resumes}
    )

def analyze_resume(request, job_id):

    job = Job.objects.get(id=job_id)

    resume = Resume.objects.filter(
        user=request.user,
        job=job
    ).last()

    if not resume:
        return HttpResponse(
            "Please upload resume for this job first"
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
            found_skills.append(skill.strip())

    ats_score = int(
        (len(found_skills) / len(skills)) * 100
    )

    return render(
        request,
        'ats_result.html',
        {
            'score': ats_score,
            'skills': found_skills,
            'job': job
        }
    )


def ai_resume_feedback(request, job_id):

    from jobs.models import Job
    import PyPDF2

    job = Job.objects.get(id=job_id)

    resume = Resume.objects.filter(
        user=request.user,
        job=job
    ).last()

    if not resume:
        return HttpResponse(
            "Upload Resume First"
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

    prompt = f"""
    Analyze this resume.

    Job Role:
    {job.title}

    Required Skills:
    {job.required_skills}

    Resume Content:
    {text}

    Give:
    1. ATS Match Percentage
    2. Strengths
    3. Missing Skills
    4. Improvement Suggestions
    5. Final Recommendation
    """

    response = model.generate_content(
        prompt
    )

    feedback = response.text

    return render(
        request,
        'ai_feedback.html',
        {
            'job': job,
            'feedback': feedback
        }
    )