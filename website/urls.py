from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import vanonymous, vstudents, vteachers,vadmins

urlpatterns = [
    #Accès public
    
    path('',vanonymous.accueil, name='accueil'),
    path('login/', auth_views.LoginView.as_view()),
        path('contact/',vanonymous.contact, name='contact'),
        path('about/',vanonymous.Apropos, name='Apropos'),
        path('inscrit/',vstudents.StudentSignUpView.as_view(), name='inscription'),    
        path('training/',vanonymous.training, name='training'),
        path('forgetPw/',vanonymous.forgetPw, name='forgetPw'),
        path('profil/',vanonymous.profil, name='profil'),
    
    
    #Fonctions teacher
    path('teachers/', include(([
        path('', vteachers.teacher_home, name='teahome'),
        path('course/list/',vteachers.CoursesListView.as_view(), name='course_list'),
        path('course/listj/',vteachers.crs_list, name='crs_listj'),

        path('chapters/<int:pk>/', vteachers.fadd_chapters, name='chapters_change_list'),
        path('chapters/add/<int:pk>/', vteachers.addchapter, name='chap'),

        path('quizes', vteachers.QuizListView.as_view(), name='quiz_change_list'),

        path('quiz/add/', vteachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', vteachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', vteachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', vteachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', vteachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', vteachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', vteachers.QuestionDeleteView.as_view(), name='question_delete'),

    ], 'classroom'), namespace='teachers')),
    


    #Fonctions student
    path('students/', include(([
        

        path('',vstudents.student_home,name='student_home'),        
        path('allcourses/',vstudents.admin_home,name='all_courses'),
        path('mycourses/',vstudents.crs_list,name='mycourses'),

        path('q',vstudents.QuizListView.as_view(), name='quiz_list'),
        path('taken/',vstudents.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/',vstudents.take_quiz, name='take_quiz'),
        path('subscribe/<int:pk>/',vstudents.subscribe, name='subscribe'),

        path('chapter/<int:cle>',vstudents.ListChapadmin, name='Chapter'),
        path('chapter/details/<int:num>',vstudents.DetailsChapAdmin, name='Chapter'),
       

    ], 'website'), namespace='students')),
    
    
    #Fonctions admin
    path('admin/', include(([
        path('',vadmins.admin_home,name='admin_home'),

        path('category/list/',vadmins.CategoryListView.as_view(), name='categories_list'),
        path('category/listj/',vadmins.categ_list, name='cat_listj'),
        path('category/add/',vadmins.CategoryCreateView.as_view(), name='categories_add'),        
        path('category/<int:pk>/',vadmins.CategoryUpdate.as_view(), name='categories_edit'),

        path('course/add/',vadmins.CourseCreateView.as_view(), name='course_add'),
        path('course/list/',vadmins.CoursesListView.as_view(), name='course_list'),
        path('course/listj/',vadmins.crs_list, name='crs_listj'),
        path('course/<int:pk>/',vadmins.CourseUpdate.as_view(), name='course_edit'),


        path('teacher/list/',vadmins.TeachersListView.as_view(), name='tch_list'),
        path('teacher/listj/',vadmins.tech_list, name='tch_listj'),
        path('teacher/add/',vadmins.TeacherSignUpView.as_view(), name='tch_add'),
        path('teacher/<int:pk>/',vadmins.TeacherUpdate.as_view(), name='tch_edit'),
        path('teacher/<int:pk>/delete',vadmins.tdelete_teacher, name='tch_delete'),


    ], 'website'), namespace='admins')), 

    
]
