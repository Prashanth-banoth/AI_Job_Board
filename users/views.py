from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from jobs.models import Application, SavedJob
from resumes.models import Resume


def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == "POST":

        username = request.POST['username'].strip()
        email = request.POST['email'].strip().lower()
        password = request.POST['password']

        username = username.capitalize()

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect('/register/')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already taken."
            )

            return redirect('/register/')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

       

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect('/login/')

    return render(
        request,
        'register.html'
    )



def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')

@login_required
@login_required
def dashboard(request):

    applications_count = Application.objects.filter(
        user=request.user
    ).count()

    saved_jobs_count = SavedJob.objects.filter(
        user=request.user
    ).count()

    resumes_count = Resume.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        'dashboard.html',
        {
            'applications_count': applications_count,
            'saved_jobs_count': saved_jobs_count,
            'resumes_count': resumes_count
        }
    )

def logout_view(request):
    logout(request)
    return redirect('/')