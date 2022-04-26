from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

"""
format 의 제한이 없이 request를 받을 수 있다.
it will, by default, return an HTML-formatted representation of the resource when that resource is requested by a web browser. 
"""
urlpatterns = format_suffix_patterns(urlpatterns)
