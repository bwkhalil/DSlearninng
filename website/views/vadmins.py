from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,UpdateView)
from ..decorators import teacher_required,admin_required
from ..forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm,CategoryCreation,CourseCreation, UserUpdateForm
from ..models import Answer, Question, Quiz, User,Category,Course,Teacher
from django.core import serializers
import json
from django.http import JsonResponse


#Home
def admin_home(request):
    return render(request, 'wbtemp/t_admins/admin_home.html')
#####################################################################

'''________________________Teachers#_____________________________'''
#_____________________________Add_____________________________#

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'wbtemp/t_admins/teacher_add.html'
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        return redirect('admins:tch_list')
#_____________________________get_____________________________#

def tech_list(request):
    data=[]
    for usr in User.objects.filter(is_teacher=True):
        user={'user_id':usr.user_id,'first_name':usr.first_name, 'last_name':usr.last_name,'username':usr.username,'email':usr.email,'last_login':usr.last_login,'date_joined':usr.date_joined}
        data.append(user)
    return JsonResponse({"data":data})
#_____________________________delete_____________________________#

def tdelete_teacher(request,pk):
    try:
        Teacher.objects.filter(user_id=int(pk)).delete()
        User.objects.filter(user_id=int(pk)).delete()
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"status": "not ok:\n"+str(e)})        
#_____________________________view_________________________________#    
class TeachersListView(ListView):
    model = Teacher
    ordering = ('first_name', )
    context_object_name = 'teachers'
    template_name = 'wbtemp/t_admins/teacher_list.html'

    def get_queryset(self):
        # Retreive all slot id for the customer with id = 1
        queryset = User.objects.all().filter(is_teacher=True)
        return queryset
#_____________________________Update__________________________________#

class TeacherUpdate(UpdateView):
        model = User
        fields = ('first_name', 'last_name','username','email',)  
        context_object_name = 'teacher'
        template_name = 'wbtemp/t_admins/teacher_edit.html'
        success_url = '/admin/teacher/list'
        

        def get_context_data(self, **kwargs):
            return super().get_context_data(**kwargs)
        def get_queryset(self):
            return super().get_queryset()


'''_____________________________Categories_____________________________'''
#_____________________________Add_____________________________________#

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreation
    template_name = 'wbtemp/t_admins/category_add.html'
    def get_context_data(self):
        return super().get_context_data()
    def form_valid(self, form):
        category = form.save()
        return redirect('admins:categories_list')
#_____________________________List_____________________________________#

class CategoryListView(ListView):
    model = Category
    ordering = ('name', )
    context_object_name = 'categories'
    template_name = 'wbtemp/t_admins/category_list.html'

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset
#_____________________________get_____________________________#

def categ_list(request):
    data=[]
    for usr in Category.objects.all():
        cat={'id':usr.id,'name':usr.name, 'description':usr.description}
        data.append(cat)
    return JsonResponse({"data":data})
#_____________________________Update__________________________________#

class CategoryUpdate(UpdateView):
        model = Category
        fields = ('name', 'description',)  
        context_object_name = 'category'
        template_name = 'wbtemp/t_admins/categorie_edit.html'
        success_url = '/admin/category/list'

        def get_context_data(self, **kwargs):
            return super().get_context_data(**kwargs)
        def get_queryset(self):
            return super().get_queryset() 

'''_____________________________Courses_____________________________'''
class CoursesListView(ListView):
    model = Course
    ordering = ('name', )
    context_object_name = 'courses'
    template_name = 'wbtemp/t_admins/course_list.html'

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseCreation
    template_name = 'wbtemp/t_admins/course_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        messages.success(self.request, 'The course was created with success')
        return redirect('admins:course_list')
#_____________________________get_____________________________#

def crs_list(request):
    data=[]
    for usr in Course.objects.all():
        cat={'id':usr.id,'name':usr.name, 'description':usr.description}
        data.append(cat)
    return JsonResponse({"data":data})
#_____________________________Update__________________________________#

class CourseUpdate(UpdateView):
        model = Course
        fields = ('name', 'description',)  
        context_object_name = 'category'
        template_name = 'wbtemp/t_admins/course_edit.html'
        success_url = '/admin/course/list'

        def get_context_data(self, **kwargs):
            return super().get_context_data(**kwargs)
        def get_queryset(self):
            return super().get_queryset() 