from django.urls import include, path

from website.views import vadmins, vstudents, vteachers,vanonymous

urlpatterns = [
    path('', include('website.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', vstudents.StudentSignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', vstudents.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', vadmins.TeacherSignUpView.as_view(), name='teacher_signup'),
]
