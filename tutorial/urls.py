from django.urls import include, path
from rest_framework import routers

from quickstart import views

# view가 아닌 viewset을 사용하므로 url 생성을 하기 위해서 라우터에 등록해야 한다.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]