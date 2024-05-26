from django.urls import path, include, re_path

from activityngo.website_content import web

app_name = 'website_content__app'

urlpatterns = [
    path('', web.website_content_pages, name='get-student-index-page'),
    # re_path(r'^(what|where|how|list|who)/$', web.website_content_pages, name='website_content_pages'),
    path('what/', web.website_content_pages, name='what'),
    path('where/', web.website_content_pages, name='where'),
    path('how/', web.website_content_pages, name='how'),
    path('who/', web.website_content_pages, name='who'),
    path('list/', web.website_content_pages, name='list'),


]
