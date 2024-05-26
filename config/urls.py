"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', include('activityngo.student.web_urls')),  # static student website
    path(
        "api/",
        include(
            [
                path("custom-auth/", include("activityngo.custom_auth.api_urls")),
                path("ngo/", include("activityngo.ngo.api_urls")),
                path("registration/", include("activityngo.registrations.api_urls")),
                path("sub-admin/", include("activityngo.sub_admin.api_urls")),
                path("entities/", include("activityngo.entities.api_urls")),
                path("university/", include("activityngo.university.api_urls")),
                path("college/", include("activityngo.college.api_urls")),
                path("project/", include("activityngo.project.api_urls")),
                path("question-types/", include("activityngo.question_types.api_urls")),
                path("student/", include("activityngo.student.api_urls")),
                path("notification/", include("activityngo.notification.api_urls")),
                path("cart/", include("activityngo.cart.api_urls")),
                path("discount/", include("activityngo.discount.api_urls")),
                path("order/", include("activityngo.order.api_urls")),
                path(
                    "student-project/", include("activityngo.student_project.api_urls")
                ),
                path(
                    "dashboard-count/", include("activityngo.dashboardcount.api_urls")
                ),
                path("cms/", include("activityngo.cms.api_urls")),
                path(
                    "activity-report/", include("activityngo.activity_report.api_urls")
                ),
                path("fcm/", include("activityngo.fcm.api_urls")),
                path("activity-email/", include("activityngo.activity_email.api_urls")),
                path(
                    "task-evaluation/", include("activityngo.task_evaluation.api_urls")
                ),
                path("resubmit-task/", include("activityngo.resubmit_task.api_urls")),
                path("website-content/", include("activityngo.website_content.api_urls")),
            ]
        ),
    ),
    path('student/', include([
        path('', include('activityngo.student.web_urls')),
        path('verification/', include('activityngo.order.web_urls')),
    ])),
    path('', include([
            path('', include('activityngo.website_content.web_urls')),
        ])),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
