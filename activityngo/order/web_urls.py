from django.urls import path, include, re_path

from activityngo.order import web

app_name = 'order_app'

urlpatterns = [
    path('<str:encrypted_id>/', web.GetStudentVerificationPage, name='student-verification-order-details'),
]
