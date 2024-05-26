from django.urls import path, include, re_path

from activityngo.student import web

app_name = 'student__app'

urlpatterns = [
    # path('', web.get_student_index_page, name='get-student-index-page'),
    path('account-deletion-instructions/', web.get_student_deletion_instructions, name='get-student-deletion-instructions'),
]
