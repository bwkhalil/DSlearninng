from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
import json
from ..decorators import student_required,admin_required
from ..forms import StudentSignUpForm, TakeQuizForm,TeacherInterestsForm
from ..models import Category, Chapter, Course, Media, Quiz, Student, TakenQuiz, User,Subcription
from datetime import datetime
def student_home(request):
    return render(request, 'wbtemp/t_students/student_home.html')

#_____________________________get all courses_____________________________#
def admin_home(request):
    category=Category.objects.all()
    student = request.user.student
    #les cours aux quels l'etudiant en cours est inscrit
    student_interests =student.subjects.values_list('pk', flat=True)
    data=[]
    for c in category:
        cours=Course.objects.filter(categorie_id=c.id).exclude(pk__in=student_interests) 
        if cours:
            data.append({"category":c.name,"courses":cours})
    #cours=category.cours_set.all()
    context={'cat':data}
    return render(request, 'wbtemp/t_students/course_list.html',context)

def ListChapadmin(request ,cle):
    data=[]
    ch=Chapter.objects.filter(course_id=cle)
    for chap in ch:
        queryset=Media.objects.all().get(chapter_id=chap.id)
        print(queryset.nom)
        data.append({"chapter":chap.name,"video":queryset.nom})
    return render(request, 'wbtemp/t_students/view_chapter.html',{'chapitres':data})
    
    


def DetailsChapAdmin(request,num):
    det=Chapter.objects.all().filter(num=num)
    return render(request, 'wbtemp/t_students/details_chap.html',{'khra':det})

def crs_list(request):
    category=Category.objects.all()
    student = request.user.student
    #les cours aux quels l'etudiant en cours est inscrit
    student_interests =student.subjects.values_list('pk', flat=True)
    data=[]
    for c in category:
        cours=Course.objects.filter(categorie_id=c.id,pk__in=student_interests)
        if cours:
            data.append({"category":c.name,"courses":cours})
    #cours=category.cours_set.all()
    context={'cat':data}
    return render(request, 'wbtemp/t_students/mycourses.html',context)
   
    
#_____________________________get my courses_____________________________#

def my_courses(request):
    
    student = request.user.student
    student_interests =student.subjects.values_list('pk', flat=True)
    
    #for usr in Course.objects.filter(pk__in=student_interests):
    
    data=[]
    for usr in Course.objects.filter(pk__in=student_interests):
        cat={'id':usr.id,'name':usr.name, 'description':usr.description}
        data.append(cat)
    return JsonResponse({"data":data})

def subscribe(request,pk):
    msg=""
    try:
        student=request.user.student
        course_id=int(pk)
        course=Course.objects.get(pk=course_id)
        sub_date=datetime.now()
        Subcription.objects.create(student=student,subject=course,subscription_date=sub_date)
        msg="ok"
    except Exception as e:
        msg=str(e)
        
    return JsonResponse({'message':msg})

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:all_courses')


@method_decorator([login_required, admin_required], name='dispatch')
class TeacherInterestsView(UpdateView):
    model = Student
    form_class =TeacherInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'wbtemp/t_students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.subjects.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'wbtemp/t_students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.quizzes \
            .prefetch_related('subject', 'subject') \
            .order_by('subject__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })
