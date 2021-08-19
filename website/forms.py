from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models.enums import TextChoices
from django.forms import ModelForm
from django.forms.utils import ValidationError
from website.models import *
from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout, Div, Field, Row, Submit, Button, Column
from crispy_forms.helper import FormHelper
#Validator: les controles de saisie
def validate_even(pname):
    if not all(x.isalpha() or x.isspace() for x in pname):
        raise ValidationError(('%(value)s is not a person name'),params={'value': pname},)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email',) 
        
class TeacherSignUpForm(UserCreationForm):
    Courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    email = forms.EmailField(required=True)
    first_name=forms.CharField(required=True,validators=[validate_even])
    last_name=forms.CharField(required=True,validators=[validate_even])
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name","last_name","username", "email", "password1", "password2")

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name=self.cleaned_data["first_name"]
        user.last_name=self.cleaned_data["last_name"]
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.subjects.add(*self.cleaned_data.get('Courses'))        
        return user

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name=forms.CharField(required=True,validators=[validate_even])
    last_name=forms.CharField(required=True,validators=[validate_even])
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user

class TeacherInterestsForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('subjects', )
        widgets = {'Courses': forms.CheckboxSelectMultiple}

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )

class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')

class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')

class CategoryCreation(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class CourseCreation(forms.ModelForm):
    categorie = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )
    class Meta:
        model=Course
        fields = ("name","description","categorie")
class QuizzCreation(forms.ModelForm):
    subjects = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )
    class Meta:
        model=Course
        fields = ("name","description","categorie")
    
    
    
    
