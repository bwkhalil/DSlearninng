from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user_id)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Course(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff')
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subjects=models.ManyToManyField(Course,through='teacher_courses')

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subjects=models.ManyToManyField(Course,through='Subcription')
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username

class Subcription(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subcription_student')
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subcription_session')
    subscription_date=models.DateTimeField(verbose_name="Subscription date")

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text

class Teacher_Courses(models.Model):
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="teaching")
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name="teaching")

class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='who_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')



class Chapter(models.Model):
    #id=models.AutoField(primary_key=True)
    num=models.IntegerField()
    name=models.CharField(max_length=150)
    description=models.TextField(blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='course_chapters')

class Media(models.Model):
    nom=models.CharField(max_length=255)
    filetype=models.CharField(max_length=50)
    chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE,related_name='chapter_files')
