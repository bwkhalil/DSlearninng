from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,UpdateView)
from ..decorators import teacher_required
from ..forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm
from ..models import Answer, Chapter, Course, Question, Quiz, Teacher, User,Media
import json
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.template import RequestContext

def teacher_home(request):
    return render(request, 'wbtemp/t_teacher/admin_home.html')
@csrf_exempt
def fadd_chapters(request,pk):
    csrfContext= RequestContext(request)
    context={'cours':pk,"ddd":csrfContext}
    
    return render(request, 'wbtemp/t_teachers/chapter_add_form.html',context)
@csrf_exempt
def addchapter(request,pk):
    uc = request.POST
    body = uc
    print(body)
    num = body['num']
    name = body['name']
    desc = body['description']
    myfile =request.FILES['fileData']
    fs = FileSystemStorage()
    ext=myfile.name.split('.')[-1]
   
    course=Course.objects.get(pk=pk)
    filename = fs.save("static/courses/"+course.name+"/Chapter_"+str(num[0])+"_"+name+"."+ext, myfile)
    chapter=Chapter.objects.create(name=name,num=num,description=desc,course=course)
    uploaded_file_url = fs.url(filename)
    media=Media.objects.create(nom="courses/"+course.name+"/Chapter_"+str(num[0])+"_"+name+"."+ext,filetype=ext,chapter=chapter)
    return JsonResponse({"message":"ok"})
    

#his courses
@method_decorator([login_required, teacher_required], name='dispatch')
class CoursesListView(ListView):
    model = Course
    ordering = ('name', )
    context_object_name = 'courses'
    template_name = 'wbtemp/t_teachers/course_list.html'

    def get_queryset(self):
        """ teacher = self.request.user.teacher
        student_interests =teacher.subjects.values_list('pk', flat=True)
        queryset = self.request.user.subjects.select_related('course')
        print(queryset) """
        teacher = self.request.user.teacher
        student_interests =teacher.subjects.values_list('pk', flat=True)
        queryset = student_interests
        return queryset
def crs_list(request):
    data=[]
    teacher = request.user.teacher
    student_interests =teacher.subjects.values_list('pk', flat=True)
    for usr in Course.objects.filter(pk__in=student_interests):
        cat={'id':usr.id,'name':usr.name, 'description':usr.description}
        data.append(cat)
    return JsonResponse({"data":data})

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'wbtemp/t_teachers/quiz_change_list.html'

    def get_queryset(self):
        teacher = self.request.user
        teacher=Teacher.objects.get(pk=teacher.user_id)
        student_interests =teacher.subjects.values_list('pk', flat=True)
        #pk__in=student_interests
        return Quiz.objects.filter(subject__in=student_interests)



@method_decorator([login_required, teacher_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'subject', )
    template_name = 'wbtemp/t_teachers/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('teachers:quiz_change', quiz.pk)
       


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'subject', )
    context_object_name = 'quiz'
    template_name = 'wbtemp/t_teachers/quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        teacher = self.request.user
        teacher=Teacher.objects.get(pk=teacher.user_id)
        student_interests =teacher.subjects.values_list('pk', flat=True)
        #pk__in=student_interests
        return Quiz.objects.filter(subject__in=student_interests)

    def get_success_url(self):
        return reverse('teachers:quiz_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'wbtemp/t_teachers/quiz_delete_confirm.html'
    success_url = reverse_lazy('teachers:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'wbtemp/t_teachers/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        teacher = self.request.user
        teacher=Teacher.objects.get(pk=teacher.user_id)
        student_interests =teacher.subjects.values_list('pk', flat=True)
        #pk__in=student_interests
        return Quiz.objects.filter(subject__in=student_interests)

@login_required
@teacher_required
def teacher_home(request):
    return render(request, 'wbtemp/t_teachers/teacher_home.html')



@login_required
@teacher_required
def question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('teachers:question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'wbtemp/t_teachers/question_add_form.html', {'quiz': quiz, 'form': form})


@login_required
@teacher_required
def question_change(request, quiz_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('teachers:quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'wbtemp/t_teachers/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'wbtemp/t_teachers/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('teachers:quiz_change', kwargs={'pk': question.quiz_id})
