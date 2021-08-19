from django.shortcuts import redirect, render
from django.views.generic import TemplateView


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'wbtemp/teachers/home.html')
        elif request.user.is_admin:
            return render(request, 'wbtemp/admins/home.html')
        else:
            return render(request, 'wbtemp/students/home.html')
    return render(request, 'wbtemp/home.html')

def contact(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'wbtemp/teachers/home.html')
        elif request.user.is_admin:
            return render(request, 'wbtemp/admins/home.html')
        else:
            return render(request, 'wbtemp/students/home.html')
    return render(request, 'wbtemp/contact.html')

def courses(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'wbtemp/teachers/home.html')
        elif request.user.is_admin:
            return render(request, 'wbtemp/admins/home.html')
        else:
            return render(request, 'wbtemp/students/home.html')
    return render(request, 'wbtemp/courses.html')

def teachers(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'wbtemp/teachers/home.html')
        elif request.user.is_admin:
            return render(request, 'wbtemp/admins/home.html')
        else:
            return render(request, 'wbtemp/students/home.html')
    return render(request, 'wbtemp/teachers.html')

def fiche_teacher(request,pk):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'wbtemp/teachers/home.html')
        elif request.user.is_admin:
            return render(request, 'wbtemp/admins/home.html')
        else:
            return render(request, 'wbtemp/students/home.html')
    return render(request, 'wbtemp/teachers.html')
from django.shortcuts import render
from django.http import HttpResponse


def accueil(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'wbtemp/t_teachers/teacher_home.html')
        elif request.user.is_admin:
            return render(request, 'wbtemp/t_admins/admin_home.html')
        else:
            return render(request, 'wbtemp/t_students/student_home.html')
    return render(request, 'wbtemp/t_anonymous/accueil.html')
    


def contact(request):
    return render(request, "wbtemp/t_anonymous/Contact.html")


def Apropos(request):
    return render(request, "wbtemp/t_anonymous/Apropos.html")


def inscription(request):
    return render(request, "wbtemp/t_anonymous/inscription.html")


def login(request):
    return render(request, "wbtemp/t_anonymous/login.html")


def training(request):
    return render(request, "wbtemp/t_anonymous/Training.html")


def forgetPw(request):
    return render(request, "wbtemp/t_anonymous/oblieMDP.html")


def profil(request):
    return render(request, "wbtemp/t_anonymous/ProfilUser.html")




