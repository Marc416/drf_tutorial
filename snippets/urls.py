from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>', views.snippet_detail),
]
# format 의 제한이 없ㅍ
urlpatterns = format_suffix_patterns(urlpatterns)

